# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.source.models import Stock
from apps.source.models import StockDailyData
from apps.source.models import TradeCalendar
import tushare as ts
import threading
import math
import time
import logging


class Command(BaseCommand):
    help = '获取股票日数据'
    thread_num = 10  # 线程数
    all = False  # 是否获取全部数据
    start_at = None  # 命令行传入的开始日期
    end_at = None  # 命令行传入的结束日期
    api_times_pm = 500  # api每分钟请求限制
    thread_api_freq = 0  # 每个线程请求api的频率
    stocks = []  # 命令行传入的股票代码
    stock_objs = []  # 股票集合
    last_date = ''  # 从api获取数据时默认的截止日期
    last_trade_date = ''  # 上一个交易日

    def __init__(self):
        self.logger = logging.getLogger('log')
        ts.set_token(settings.TUSHARE_API_TOKEN)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--all', action='store_true', dest='all', help='是否拉取全部数据')
        parser.add_argument('--stocks', dest='stocks', help='拉取某些股票的数据')
        parser.add_argument('--start', dest='start_at', help='起始日期')
        parser.add_argument('--end', dest='end_at', help='结束日期')
        parser.add_argument('--tn', dest='thread_num', help='线程数', type=int)

    def handle(self, *args, **options):
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']获取股票日数据脚本开始：')
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
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']获取股票日数据脚本结束。')

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
        # 获取全部数据
        if self.all:
            return self.get_stock_all_data(stock)
        # 获取上一个交易日的数据，判断是否要拉取全部数据
        try:
            stock_last_trade = StockDailyData.objects.filter(ts_code=stock.ts_code,
                                                             trade_date=self.last_trade_date).get()
        except StockDailyData.DoesNotExist:
            return self.get_stock_all_data(stock)

        data = ts.pro_bar(ts_code=stock.ts_code, adj='qfq', start_date=self.last_trade_date,
                          end_date=self.last_trade_date)
        if float(stock_last_trade.close) != data.loc[0]['close']:
            print('数据库中上个交易日的数据与api获取的不一致')
            return self.get_stock_all_data(stock)
        # 如果传了start和end参数，则获取这个区间的数据，否则是获取上个交易日到截止日期的数据
        start_at = self.last_trade_date
        if self.start_at:
            start_at = self.start_at
        end_at = self.last_date
        if self.end_at:
            end_at = self.end_at
        print('[' + stock.ts_code + ']' + stock.name + '[' + start_at + '~' + end_at + ']')
        self.get_stock_data(stock=stock, start_date=start_at, end_date=end_at)

    def get_stock_all_data(self, stock):
        start_at = stock.list_date
        end_at = self.last_date
        print('[' + stock.ts_code + ']' + stock.name + '，拉取股票全部数据[' + start_at + '~' + end_at + ']')
        self.get_stock_data(stock=stock, start_date=start_at, end_date=end_at)

    def get_stock_data(self, stock, start_date, end_date):
        """
        获取股票数据，每次最多获取5000条，每分钟最多请求500次
        :param stock: stock model对象
        :param start_date: 开始日期，格式Ymd，例如19991118
        :param end_date: 结束日期，格式Ymd，例如19991118
        :return:
        """
        try:
            # 在起始日期和结束日期之间，每20年循环一次
            start_obj = datetime.strptime(start_date, '%Y%m%d')
            end_obj = datetime.strptime(end_date, '%Y%m%d')
            while start_obj.__le__(end_obj):
                while_start_at = datetime.now()
                after_20_years = start_obj + relativedelta(years=20)
                if after_20_years.__lt__(end_obj):
                    print('[' + stock.ts_code + ']' + stock.name + '[' + start_obj.strftime(
                        '%Y%m%d') + '~' + after_20_years.strftime(
                        '%Y%m%d') + ']')
                    data = ts.pro_bar(ts_code=stock.ts_code, adj='qfq', start_date=start_obj.strftime('%Y%m%d'),
                                      end_date=after_20_years.strftime('%Y%m%d'))
                    start_obj = after_20_years + relativedelta(days=1)
                else:
                    print('[' + stock.ts_code + ']' + stock.name + '[' + start_obj.strftime(
                        '%Y%m%d') + '~' + end_obj.strftime(
                        '%Y%m%d') + ']')
                    data = ts.pro_bar(ts_code=stock.ts_code, adj='qfq', start_date=start_obj.strftime('%Y%m%d'),
                                      end_date=end_obj.strftime('%Y%m%d'))
                    start_obj = end_obj + relativedelta(days=1)
                # 写入数据到数据库
                if data is None:
                    print("数据为None")
                    continue
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
                    StockDailyData.objects.update_or_create(defaults=dict(item), ts_code=item['ts_code'],
                                                            trade_date=item['trade_date'])
                time_interval = (datetime.now() - while_start_at).seconds + 1
                if time_interval < self.thread_api_freq:
                    diff = self.thread_api_freq - time_interval
                    print('循环花了', time_interval, '秒，没有超过频率限制', self.thread_api_freq, '秒，睡眠', diff, '秒')
                    time.sleep(diff)
        except IOError:
            self.log("请求频繁，睡眠10秒后继续请求")
            time.sleep(10)
            self.get_stock_data(stock=stock, start_date=start_date, end_date=end_date)

    def init_params(self, args, options):
        if options['thread_num']:
            self.thread_num = options['thread_num']
        self.all = options['all']
        if options['stocks']:
            self.stocks = options['stocks'].split(',')
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
        # 计算每个线程请求api的频率
        thread_times_pm = math.floor(self.api_times_pm / self.thread_num)
        self.thread_api_freq = math.ceil(60 / thread_times_pm)

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
