# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from datetime import datetime
from utils import constants
from django.db.models import Max
from apps.source.models import Stock
from apps.source.models import TradeCalendar
from apps.source.models import IndexDailyData
from apps.source.models import StockDailyData
import logging
import threading


class Command(BaseCommand):
    help = '获取持续强势的股票'
    start_date = None  # 起始日期
    end_date = None  # 结束日期
    days = 3  # 天数
    max_rate = None  # 最大涨幅
    thread_num = 20  # 线程数
    stocks = []  # 股票集合

    def __init__(self):
        self.logger = logging.getLogger('log')

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--start', dest='start_at', help='起始日期')
        parser.add_argument('--days', dest='days', help='天数')
        parser.add_argument('--tn', dest='thread_num', help='线程数', type=int)

    def handle(self, *args, **options):
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetContinuedStrongStock]脚本开始：')
        try:
            self.init_params(args=args, options=options)
            self.stocks = list(Stock.objects.values('ts_code').all())
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
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetContinuedStrongStock]脚本结束。')

    def cycle_get_queue(self):
        """
        循环处理数据
        :return:
        """
        while 0 < self.stocks.__len__():
            stock = self.stocks.pop(0)
            if stock:
                self.calc_one_stock(stock['ts_code'])
            else:
                return

    def calc_one_stock(self, ts_code):
        pass

    def init_params(self, args, options):
        """
        初始化脚本参数
        :param args:
        :param options:
        :return:
        """
        # 计算多少天
        if options['days']:
            self.days = options['days']
        # 计算起始日期
        if options['start_at']:
            self.start_date = options['start_at']
        else:
            today = datetime.now().strftime('%Y%m%d')
            self.start_date = TradeCalendar.objects.filter(cal_date__lte=today, is_open=1).order_by('-id').values_list('cal_date').first()[0]
        # 计算结束日期
        end_date = TradeCalendar.objects.filter(cal_date__lte=self.start_date, is_open=1).order_by('-id').values_list('cal_date')[self.days-1:self.days]
        self.end_date = end_date.first()[0]
        # 计算三个指数的最大涨幅
        self.max_rate = IndexDailyData.objects.filter(ts_code__in=constants.NORMAL_INDEXES,
                                                      trade_date=self.start_date).aggregate(Max('pct_chg'))[
            'pct_chg__max']
        # 线程数
        if options['thread_num']:
            self.thread_num = options['thread_num']

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
