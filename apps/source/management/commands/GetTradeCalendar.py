# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from apps.source.models import TradeCalendar
import tushare as ts
import logging


class Command(BaseCommand):
    help = '获取交易日历列表'
    fields = [
        'exchange',
        'cal_date',
        'is_open',
        'pretrade_date',
    ]

    def __init__(self):
        self.logger = logging.getLogger('log')
        self.token = settings.TUSHARE_API_TOKEN
        ts.set_token(self.token)

    def handle(self, *args, **options):
        pro = ts.pro_api()

        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetTradeCalendar]脚本开始：')
        try:
            data = pro.trade_cal(fields=','.join(self.fields))
            for index, item in data.iterrows():
                TradeCalendar.objects.update_or_create(defaults=dict(item), exchange=item['exchange'], cal_date=item['cal_date'])
        except Exception as e:
            self.log('程序出现异常:' + str(e))
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetTradeCalendar]脚本结束。')

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
