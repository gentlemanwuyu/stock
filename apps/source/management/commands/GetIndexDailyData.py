# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.source.models import Index
from apps.source.models import IndexDailyData
from queue import Queue
from threading import Thread
import tushare as ts
import math


class Command(BaseCommand):
    help = '获取指数日数据'

    def __init__(self):
        self.all = False
        self.indexes = []
        self.start_at = None
        self.end_at = None
        self.queue = Queue()
        self.token = settings.TUSHARE_API_TOKEN
        ts.set_token(self.token)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--all', action='store_true', dest='all', help='是否拉取所有数据')
        parser.add_argument('--indexes', dest='indexes', help='拉取某些指数的数据')
        parser.add_argument('--start', dest='start_at', help='起始日期')
        parser.add_argument('--end', dest='end_at', help='结束日期')

    def handle(self, *args, **options):
        print('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']开始获取指数日数据')
        # 初始化脚本参数
        self.init_params(args=args, options=options)
        try:
            ts.set_token(self.token)
            # 查询符合条件的指数
            query = Index.objects
            if self.indexes:
                query = query.filter(ts_code__in=self.indexes)
            indexes = query.all()
            # 将指数写入队列
            for index in indexes:
                self.queue.put(index)
            for i in range(10):
                thread = Thread(target=self.cycle_get_queue)
                thread.start()
        except Exception as e:
            print('[Exception]' + str(e))
        print('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']获取指数日数据结束')

    def cycle_get_queue(self):
        while True:
            index = self.queue.get()
            if index:
                self.handle_one_index(index)
            else:
                return

    def handle_one_index(self, index):
        """
        处理一个指数的数据
        :param index:
        :return:
        """
        # 计算起始日期与结束日期
        start_at = datetime.now().strftime('%Y%m%d')
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
            after_30_years = start_date + relativedelta(years=30)
            if after_30_years.__lt__(end_date):
                print(index.ts_code + index.name + '[' + start_date.strftime('%Y%m%d') + '~' + after_30_years.strftime(
                    '%Y%m%d') + ']')
                data = ts.pro_bar(ts_code=index.ts_code, asset='I', start_date=start_date.strftime('%Y%m%d'),
                                  end_date=after_30_years.strftime('%Y%m%d'))
                start_date = after_30_years + relativedelta(days=1)
            else:
                print(index.ts_code + index.name + '[' + start_date.strftime('%Y%m%d') + '~' + end_date.strftime(
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

    def init_params(self, args, options):
        self.all = options['all']
        if options['indexes']:
            self.indexes = options['indexes'].split(',')
        if options['start_at']:
            self.start_at = options['start_at']
        if options['end_at']:
            self.end_at = options['end_at']
