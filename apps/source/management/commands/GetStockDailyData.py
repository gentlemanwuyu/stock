from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from apps.source.models import Stock
from apps.source.models import StockDailyData
import tushare as ts


class Command(BaseCommand):
    help = '获取股票日数据'

    def __init__(self):
        self.all = False
        self.stocks = []
        self.start_at = None
        self.end_at = None
        self.token = settings.TUSHARE_API_TOKEN
        self.ts = ts.set_token(self.token)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--all', action='store_true', dest='all', help='是否拉取所有数据')
        parser.add_argument('--stocks', dest='stocks', help='拉取某些股票的数据')
        parser.add_argument('--start', dest='start_at', help='起始日期')
        parser.add_argument('--end', dest='end_at', help='结束日期')

    def handle(self, *args, **options):
        print('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']开始获取股票日数据')
        # 初始化脚本参数
        self.init_params(args=args, options=options)
        try:
            ts.set_token(self.token)
            # 查询符合条件的股票
            query = Stock.objects
            if self.stocks:
                query = query.filter(ts_code__in=self.stocks)
            stocks = query.all()
            for stock in stocks:
                self.handle_one_stock(stock)
        except Exception as e:
            print('[Exception]' + str(e))
        print('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']获取股票日数据结束')

    def handle_one_stock(self, stock):
        start_at = datetime.now().strftime('%Y%m%d')
        if self.all:
            start_at = stock.list_date
        elif self.start_at:
            start_at = self.start_at
        end_at = datetime.now().strftime('%Y%m%d')
        if self.end_at:
            end_at = self.end_at
        print(stock.ts_code + stock.name + '[' + start_at + '~' + end_at + ']')
        data = ts.pro_bar(ts_code=stock.ts_code, adj='qfq', start_date=start_at, end_date=end_at)
        for index, item in data.iterrows():
            StockDailyData.objects.update_or_create(defaults=dict(item), ts_code=item['ts_code'],
                                                    trade_date=item['trade_date'])

    def init_params(self, args, options):
        self.all = options['all']
        if options['stocks']:
            self.stocks = options['stocks'].split(',')
        if options['start_at']:
            self.start_at = options['start_at']
        if options['end_at']:
            self.end_at = options['end_at']
