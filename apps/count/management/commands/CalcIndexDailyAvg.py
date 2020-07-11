# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.source.models import Index
from apps.source.models import TradeCalendar
from apps.source.models import IndexDailyData
from apps.count.models import IndexDailyAvg
import threading
import logging


class Command(BaseCommand):
    help = '计算指数日线平均数据'
    thread_num = 10  # 线程数
    periods = [5, 10, 20, 30, 60, 200]  # 平均线计算周期
    max_period = 200  # 最大计算周期
    all = False  # 是否获取全部数据
    start_at = None  # 命令行传入的开始日期
    end_at = None  # 命令行传入的结束日期
    indexes = []  # 命令行传入的股票代码
    index_objs = []  # 指数集合
    last_date = ''  # 默认的截止日期
    last_trade_date = ''  # 上一个交易日
    trade_dates = []

    def __init__(self):
        self.logger = logging.getLogger('log')

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--all', action='store_true', dest='all', help='是否拉取全部数据')
        parser.add_argument('--indexes', dest='indexes', help='计算某些指数的数据')
        parser.add_argument('--start', dest='start_at', help='起始日期')
        parser.add_argument('--end', dest='end_at', help='结束日期')
        parser.add_argument('--tn', dest='thread_num', help='线程数', type=int)

    def handle(self, *args, **options):
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']计算指数日平均数据脚本开始：')
        try:
            self.init_params(args=args, options=options)
            # 查询符合条件的指数
            query = Index.objects
            if self.indexes:
                query = query.filter(ts_code__in=self.indexes)
            indexes = query.all()
            self.index_objs = list(indexes)
            # 多线程计算数据
            thread_list = []
            for i in range(self.thread_num):
                t = threading.Thread(target=self.cycle_handle_index)
                thread_list.append(t)
            for t in thread_list:
                t.setDaemon(True)
                t.start()
            for t in thread_list:
                t.join()
        except Exception as e:
            self.log('程序出现异常:' + str(e))
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']计算指数日平均数据脚本结束。')

    def cycle_handle_index(self):
        """
        循环处理一个指数
        :return:
        """
        while 0 < self.index_objs.__len__():
            index = self.index_objs.pop(0)
            if index:
                self.calc_one_index(index=index)
            else:
                return

    def calc_one_index(self, index):
        """
        计算一个指数的数据
        :param index:
        :return:
        """
        start_at = self.last_trade_date
        end_at = self.last_date
        if self.all:
            start_at = index.list_date
        else:
            if self.start_at:
                start_at = self.start_at
            if self.end_at:
                end_at = self.end_at
        return self.calc_index(index=index, start_at=start_at, end_at=end_at)

    def calc_index(self, index, start_at, end_at):
        start = datetime.strptime(start_at, '%Y%m%d')
        end = datetime.strptime(end_at, '%Y%m%d')
        while start.__le__(end):
            curr_date = start.strftime('%Y%m%d')
            if curr_date in self.trade_dates:
                data = IndexDailyData.objects.filter(ts_code=index.ts_code,
                                                     trade_date__lte=curr_date).order_by('-trade_date')[
                       :self.max_period]
                # 如果第一个对象的trade_date不等于curr_date，说明当天没有数据，则跳过
                if data.__len__() > 0 and curr_date == data[0].trade_date:
                    item = {}
                    for period in self.periods:
                        period_data = data[:period]
                        if period_data.__len__() == period:
                            period_close_data = list(map(lambda i: i.close, period_data))
                            period_close_avg = round(sum(period_close_data) / period, 2)
                            item['p' + str(period)] = period_close_avg
                            period_amount_data = list(map(lambda i: i.amount, period_data))
                            period_amount_avg = round(sum(period_amount_data) / period, 4)
                            item['a' + str(period)] = period_amount_avg
                    if item:
                        item['ts_code'] = index.ts_code
                        item['trade_date'] = curr_date
                        IndexDailyAvg.objects.update_or_create(defaults=dict(item), ts_code=item['ts_code'],
                                                               trade_date=item['trade_date'])
            # 日期加一天
            start = start + relativedelta(days=1)

    def init_params(self, args, options):
        """
        初始化参数
        :param args:
        :param options:
        :return:
        """
        if options['thread_num']:
            self.thread_num = options['thread_num']
        self.all = options['all']
        if options['indexes']:
            self.indexes = options['indexes'].split(',')
        if options['start_at']:
            self.start_at = options['start_at']
        if options['end_at']:
            self.end_at = options['end_at']
        # 计算截止日期
        today = datetime.now().strftime('%Y%m%d')
        if datetime.now().__ge__(datetime.strptime(today + ' 17:00:00', '%Y%m%d %H:%M:%S')):
            self.last_date = datetime.now().strftime('%Y%m%d')
        else:
            yesterday = datetime.now() - relativedelta(days=1)
            self.last_date = yesterday.strftime('%Y%m%d')

        trade_calendar = TradeCalendar.objects.filter(exchange='SSE', cal_date=today).get()
        if not trade_calendar:
            raise Exception("获取今天日历失败")
        self.last_trade_date = trade_calendar.pretrade_date
        # 取出所有的交易日期
        trade_dates = TradeCalendar.objects.filter(is_open=1).values_list('cal_date', flat=True)
        self.trade_dates = list(trade_dates)

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
