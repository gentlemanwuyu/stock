# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from datetime import datetime
from apps.source.models import Stock
from apps.source.models import StockName
import tushare as ts
import logging
import time


class Command(BaseCommand):
    help = '获取股票曾用名'
    fields = [
        'ts_code',
        'name',
        'start_date',
        'end_date',
        'ann_date',
        'change_reason',
    ]
    pro = None

    def __init__(self):
        self.logger = logging.getLogger('log')
        self.token = settings.TUSHARE_API_TOKEN
        ts.set_token(self.token)
        self.pro = ts.pro_api()

    def handle(self, *args, **options):
        # 清空表
        # connection.cursor().execute("TRUNCATE TABLE `stock_names`")
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetStockNameChange]脚本开始：')
        stocks = Stock.objects.values('ts_code').all()
        for stock in stocks:
            self.get_stock_name(stock['ts_code'])
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetStockNameChange]脚本结束。')

    def get_stock_name(self, ts_code):
        try:
            data = self.pro.namechange(ts_code=ts_code, fields=','.join(self.fields))
            for index, item in data.iterrows():
                StockName.objects.update_or_create(defaults=dict(item), ts_code=item['ts_code'],
                                                   start_date=item['start_date'])
        except Exception as e:
            print("请求频繁，睡眠10秒后继续请求")
            time.sleep(10)
            self.get_stock_name(ts_code=ts_code)

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
