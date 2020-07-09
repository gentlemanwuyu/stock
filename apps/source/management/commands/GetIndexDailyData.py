# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.source.models import Index
from apps.source.models import IndexDailyData
from apps.source.models import TradeCalendar
import threading
import tushare as ts
import math
import time
import logging


class Command(BaseCommand):
    help = '获取指数日数据'
    thread_num = 10  # 线程数
    all = False  # 是否获取全部数据
    indexes = []  # 命令行传入的指数代码
    index_objs = []  # 指数列表
    start_at = None  # 命令行传入的起始日期
    end_at = None  # 命令行传入的结束时间
    api_times_pm = 100  # api每分钟请求限制
    thread_api_freq = 0  # 每个线程请求api的频率
    last_2_trade_date = None  # 今日倒数第二个交易日

    def __init__(self):
        self.logger = logging.getLogger('log')
        ts.set_token(settings.TUSHARE_API_TOKEN)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--all', action='store_true', dest='all', help='是否拉取全部数据')
        parser.add_argument('--indexes', dest='indexes', help='拉取某些指数的数据')
        parser.add_argument('--start', dest='start_at', help='起始日期')
        parser.add_argument('--end', dest='end_at', help='结束日期')
        parser.add_argument('--tn', dest='thread_num', help='线程数', type=int)

    def handle(self, *args, **options):
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']获取指数日数据脚本开始：')
        # 初始化脚本参数
        self.init_params(args=args, options=options)
        try:
            # 查询符合条件的指数
            query = Index.objects
            if self.indexes:
                query = query.filter(ts_code__in=self.indexes)
            indexes = query.all()
            self.index_objs = list(indexes)
            # 多线程拉取数据
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
            self.log('[Exception]' + str(e))
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']获取指数日数据脚本结束。')

    def cycle_get_queue(self):
        while 0 < self.index_objs.__len__():
            stock = self.index_objs.pop(0)
            if stock:
                while True:
                    try:
                        self.handle_one_index(stock)
                        break
                    except IOError:
                        self.log("请求频繁，睡眠10秒后继续请求")
                        time.sleep(10)
            else:
                return

    def handle_one_index(self, index):
        """
        处理一个指数的数据
        :param index:
        :return:
        """
        # 计算起始日期与结束日期
        start_at = self.last_2_trade_date
        if self.all:
            start_at = index.list_date
        elif self.start_at:
            start_at = self.start_at
        end_at = datetime.now().strftime('%Y%m%d')
        if self.end_at:
            end_at = self.end_at
        # 在起始日期与结束日期之间，每30年循环一次
        start_date = datetime.strptime(start_at, '%Y%m%d')
        end_date = datetime.strptime(end_at, '%Y%m%d')

        while start_date.__le__(end_date):
            while_start_at = datetime.now()
            after_30_years = start_date + relativedelta(years=30)
            if after_30_years.__lt__(end_date):
                print('[' + index.ts_code + ']' + index.name + '[' + start_date.strftime(
                    '%Y%m%d') + '~' + after_30_years.strftime(
                    '%Y%m%d') + ']')
                data = ts.pro_bar(ts_code=index.ts_code, asset='I', start_date=start_date.strftime('%Y%m%d'),
                                  end_date=after_30_years.strftime('%Y%m%d'))
                start_date = after_30_years + relativedelta(days=1)
            else:
                print('[' + index.ts_code + ']' + index.name + '[' + start_date.strftime(
                    '%Y%m%d') + '~' + end_date.strftime(
                    '%Y%m%d') + ']')
                data = ts.pro_bar(ts_code=index.ts_code, asset='I', start_date=start_date.strftime('%Y%m%d'),
                                  end_date=end_date.strftime('%Y%m%d'))
                start_date = end_date + relativedelta(days=1)
            for index, item in data.iterrows():
                if math.isnan(item['open']):
                    item['open'] = 0.00
                if math.isnan(item['high']):
                    item['high'] = 0.00
                if math.isnan(item['low']):
                    item['low'] = 0.00
                if math.isnan(item['close']):
                    item['close'] = 0.00
                if math.isnan(item['pre_close']):
                    item['pre_close'] = 0.00
                if math.isnan(item['change']):
                    item['change'] = 0.00
                if math.isnan(item['pct_chg']):
                    item['pct_chg'] = 0.00
                if math.isnan(item['vol']):
                    item['vol'] = 0.00
                if math.isnan(item['amount']):
                    item['amount'] = 0.00
                IndexDailyData.objects.update_or_create(defaults=dict(item), ts_code=item['ts_code'],
                                                        trade_date=item['trade_date'])
            time_interval = (datetime.now() - while_start_at).seconds + 1
            if time_interval < self.thread_api_freq:
                diff = self.thread_api_freq - time_interval
                print('循环花了', time_interval, '秒，没有超过频率限制', self.thread_api_freq, '秒，睡眠', diff, '秒')
                time.sleep(diff)

    def init_params(self, args, options):
        self.all = options['all']
        if options['thread_num']:
            self.thread_num = options['thread_num']
        if options['indexes']:
            self.indexes = options['indexes'].split(',')
        if options['start_at']:
            self.start_at = options['start_at']
        if options['end_at']:
            self.end_at = options['end_at']
        # 计算每个线程请求api的频率
        thread_times_pm = math.floor(self.api_times_pm / self.thread_num)
        self.thread_api_freq = math.ceil(60 / thread_times_pm)
        # 计算今日倒数第二个交易日
        last_2_trade_date = TradeCalendar.objects.filter(cal_date__lt=datetime.now().strftime('%Y%m%d'),
                                                         is_open=1).values_list('cal_date').order_by('-cal_date').all()[
                            1:2]
        self.last_2_trade_date = last_2_trade_date[0][0]

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
