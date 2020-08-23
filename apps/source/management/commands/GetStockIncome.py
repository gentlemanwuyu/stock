# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from apps.source.models import Stock
from apps.source.models import StockIncome
import tushare as ts
import threading
import logging


class Command(BaseCommand):
    help = '获取股票利润表'
    fields = []
    thread_num = 50  # 线程数
    stocks = []  # 命令行传入的股票代码
    stock_objs = []  # 股票集合

    def __init__(self):
        self.logger = logging.getLogger('log')
        ts.set_token(settings.TUSHARE_API_TOKEN)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--stocks', dest='stocks', help='拉取某些股票的数据')
        parser.add_argument('--tn', dest='thread_num', help='线程数', type=int)

    def handle(self, *args, **options):
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']获取股票利润表脚本开始：')
        # 初始化脚本参数
        self.init_params(args=args, options=options)
        try:
            # 查询符合条件的股票
            query = Stock.objects
            if self.stocks:
                query = query.filter(ts_code__in=self.stocks)
            stocks = query.all()
            self.stock_objs = list(stocks)
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
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']获取股票利润表脚本结束。')

    def cycle_get_queue(self):
        while 0 < self.stock_objs.__len__():
            stock = self.stock_objs.pop(0)
            if stock:
                self.handle_one_stock(stock)
            else:
                return

    def handle_one_stock(self, stock):
        """
        处理一个股票
        :param stock:
        :return:
        """
        df = ts.pro_api().income(ts_code=stock.ts_code, fields=','.join(self.fields))
        # 将NaN替换成None
        df = df.where(df.notnull(), None)
        for index, item in df.iterrows():
            StockIncome.objects.update_or_create(defaults=dict(item), ts_code=item['ts_code'],
                                                 end_date=item['end_date'])

    def init_params(self, args, options):
        # 所有字段
        for field in StockIncome._meta.fields:
            if field.name not in ['id', 'created_at', 'updated_at']:
                self.fields.append(field.name)
        if options['thread_num']:
            self.thread_num = options['thread_num']
        if options['stocks']:
            self.stocks = options['stocks'].split(',')

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
