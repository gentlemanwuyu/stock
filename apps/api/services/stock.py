from datetime import datetime
from apps.source.models import TradeCalendar
from apps.source.models import IndexDailyData
from apps.source.models import StockDailyData
from apps.source.models import Stock
from utils.enums import IndexEnum
from django.db.models import Max
import threading
import logging
import pandas as pd


class GetContinuedStrongList:
    days = 3
    start_date = None
    trade_dates = []
    max_rates = {}
    thread_num = 100
    result = []
    stocks = []
    df = None

    def __init__(self, params):
        self.logger = logging.getLogger('log')
        if 'days' in params.keys():
            self.days = int(params['days'])
        if 'start_date' in params.keys():
            self.start_date = datetime.strptime(params['start_date'], '%Y-%m-%d').strftime('%Y%m%d')

    def handle(self):
        self.init_params()
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
        return self.result

    def cycle_get_queue(self):
        """
        循环处理数据
        :return:
        """
        while 0 < self.stocks.__len__():
            stock = self.stocks.pop(0)
            if stock:
                self.calc_one_stock(stock)
            else:
                return

    def calc_one_stock(self, stock: Stock):
        stock_daily_data = self.df[self.df.ts_code == stock['ts_code']]
        if stock_daily_data.__len__() < self.days:
            # TODO 将数据缺失的代码丢到队列中
            self.logger.info('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']股票[' + stock['ts_code'] + ']数据缺失')
            return False

        for index, stock_daily_item in stock_daily_data.iterrows():
            if stock_daily_item['pct_chg'] <= self.max_rates[stock_daily_item['trade_date']]:
                return False
        self.result.append(stock)

    def init_params(self):
        # 计算起始日期
        if not self.start_date:
            today = datetime.now().strftime('%Y%m%d')
            self.start_date = TradeCalendar.objects.filter(cal_date__lte=today, is_open=1).order_by('-id').values_list(
                'cal_date').first()[0]

        # 计算出所有的交易日
        trade_calendars = TradeCalendar.objects.filter(cal_date__lte=self.start_date, is_open=1).order_by(
            '-id').values_list(
            'cal_date')[:self.days]
        for item in trade_calendars:
            self.trade_dates.append(item[0])
            # 计算三个指数的最大涨幅
        for trade_date in self.trade_dates:
            max_rate = \
                IndexDailyData.objects.filter(ts_code__in=IndexEnum.NORMALS, trade_date=trade_date).aggregate(
                    Max('pct_chg'))['pct_chg__max']
            self.max_rates[trade_date] = float(max_rate)
        self.stocks = list(Stock.objects.values('ts_code', 'name').all())
        # 从数据库中查出所有要处理的数据，转成dataFrame
        ts_codes = [stock['ts_code'] for stock in self.stocks]
        columns = ['ts_code', 'trade_date', 'pct_chg']
        stock_daily_data = StockDailyData.objects.filter(ts_code__in=ts_codes,
                                                         trade_date__in=self.trade_dates).values_list('ts_code',
                                                                                                      'trade_date',
                                                                                                      'pct_chg').all()
        self.df = pd.DataFrame(list(stock_daily_data), columns=columns)
        self.result = []
