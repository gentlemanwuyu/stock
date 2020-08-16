# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from django_redis import get_redis_connection
from utils.enums import IndexEnum
from utils.enums import StockEnum
from utils.constants import STRONG
from utils.constants import WEAK
from django.db.models import Max
from apps.source.models import Stock
from apps.source.models import TradeCalendar
from apps.source.models import IndexDailyData
from apps.source.models import StockDailyData
import logging
import threading
import copy
import pandas as pd


class Command(BaseCommand):
    """
    计算持续强势或持续弱势的股票
    """
    help = '获取持续强势的股票'
    redis_conn = None  # redis连接
    redis_list_base_name = ''  # redis列表基础名
    start_date = None  # 起始日期
    end_date = None  # 结束日期
    days = None  # 天数集合
    max_days = None
    trade_dates = []  # 交易日期
    all_trade_dates = []  # 交易日期
    max_rates = {}  # 最大涨幅
    thread_num = 50  # 线程数
    cached = True  # 是否缓存数据
    period = 60  # 周期
    stock_codes = []  # 所有的股票代码
    df = None  # dataFrame对象
    code_poll = []  # 股票代码池
    period_trade_dates = None  # 周期交易日
    curr_calc_date = None

    def __init__(self):
        self.logger = logging.getLogger('log')

    def add_arguments(self, parser):
        parser.add_argument('--start', dest='start_at', help='起始日期')
        parser.add_argument('--days', dest='days', help='天数')
        parser.add_argument('--tn', dest='thread_num', help='线程数', type=int)
        parser.add_argument('--period', dest='period', help='计算周期', type=int)
        parser.add_argument('--output', dest='output', help='是否输出数据', action='store_true')

    def handle(self, *args, **options):
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetContinuedStock]脚本开始：')
        try:
            self.init_params(args=args, options=options)
            stocks = list(Stock.objects.values('ts_code').all())
            self.stock_codes = [item['ts_code'] for item in stocks]
            for index in range(self.period):
                self.curr_calc_date = self.trade_dates[index]
                # 删除缓存中的键
                self.delete_redis_key()
                self.period_trade_dates = self.all_trade_dates[index:index + self.max_days]
                stock_daily_data = StockDailyData.objects.filter(ts_code__in=self.stock_codes,
                                                                 trade_date__in=self.period_trade_dates).values_list(
                    'ts_code', 'trade_date', 'pct_chg').all()
                self.df = pd.DataFrame(list(stock_daily_data), columns=['ts_code', 'trade_date', 'pct_chg'])
                self.code_poll = copy.copy(self.stock_codes)
                # 多线程处理数据
                thread_list = []
                for i in range(self.thread_num):
                    t = threading.Thread(target=self.cycle_get_queue)
                    thread_list.append(t)
                for t in thread_list:
                    t.setDaemon(True)
                    t.start()
                for t in thread_list:
                    t.join()
        except Exception as e:
            self.log('程序出现异常:' + str(e))
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetContinuedStock]脚本结束。')

    def delete_redis_key(self):
        """
        删除缓存中的键
        :return:
        """
        for day in self.days:
            for strong_direction in StockEnum.STRONG_DIRECTIONS:
                strong_key = self.redis_list_base_name + str(self.curr_calc_date) + '_' + strong_direction + '_' + str(
                    day)
                if self.redis_conn.exists(strong_key):
                    self.redis_conn.delete(strong_key)
        print('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][' + str(self.curr_calc_date) + ']删除redis键结束。')

    def cycle_get_queue(self):
        """
        循环处理数据
        :return:
        """
        while 0 < self.code_poll.__len__():
            ts_code = self.code_poll.pop(0)
            if ts_code:
                self.calc_one_stock(ts_code)
            else:
                return

    def calc_one_stock(self, ts_code):
        """
        处理一个股票
        :param ts_code:
        :return:
        """
        df = self.df[self.df.ts_code == ts_code]
        for day in self.days:
            trade_dates = self.period_trade_dates[:day]
            data = df[df.trade_date.isin(trade_dates)]
            if data.__len__() < day:
                self.logger.info(
                    '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']股票[' + ts_code + ']数据缺失')
                return False
            # 强势
            strong_flag = True
            for row_index, item in data.iterrows():
                if item['pct_chg'] <= self.max_rates[item['trade_date']]:
                    strong_flag = False
                    break
            if strong_flag:
                redis_list_name = self.redis_list_base_name + str(self.curr_calc_date) + '_' + STRONG + '_' + str(day)
                self.redis_conn.rpush(redis_list_name, ts_code)
            # 弱势
            weak_flag = True
            for row_index, item in data.iterrows():
                if item['pct_chg'] >= self.max_rates[item['trade_date']]:
                    weak_flag = False
                    break
            if weak_flag:
                redis_list_name = self.redis_list_base_name + str(self.curr_calc_date) + '_' + WEAK + '_' + str(day)
                self.redis_conn.rpush(redis_list_name, ts_code)

    def init_params(self, args, options):
        """
        初始化脚本参数
        :param args:
        :param options:
        :return:
        """
        # 线程数
        if options['thread_num']:
            self.thread_num = options['thread_num']
        # redis连接
        self.redis_conn = get_redis_connection('default')
        # 计算多少天
        if options['days']:
            self.days = [int(options['days'])]
        else:
            self.days = StockEnum.CONTINUED_DAYS
        self.max_days = max(self.days)
        if options['output']:
            self.cached = False
        # 计算起始日期
        if options['start_at']:
            self.start_date = options['start_at']
        else:
            today = datetime.now().strftime('%Y%m%d')
            self.start_date = TradeCalendar.objects.filter(cal_date__lte=today, is_open=1).order_by('-id').values_list(
                'cal_date').first()[0]
        # 计算出所有的交易日
        trade_dates = TradeCalendar.objects.filter(cal_date__lte=self.start_date, is_open=1).order_by(
            '-id').values_list(
            'cal_date')[:self.period + self.max_days]
        self.all_trade_dates = [item[0] for item in trade_dates]
        self.trade_dates = self.all_trade_dates[:self.period]
        index_daily_data = IndexDailyData.objects.filter(ts_code__in=IndexEnum.NORMALS,
                                                         trade_date__in=self.all_trade_dates).values(
            'trade_date').annotate(max_rate=Max('pct_chg'))
        self.max_rates = {item['trade_date']: item['max_rate'] for item in index_daily_data}
        # redis 列表基础名
        self.redis_list_base_name = settings.CACHES['default']['KEY_PREFIX'] + ':continued_stock:'

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
