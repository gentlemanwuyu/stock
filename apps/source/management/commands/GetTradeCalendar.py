# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from apps.source.models import TradeCalendar
import tushare as ts
import math


class Command(BaseCommand):
    help = '获取交易日历列表'
    fields = [
        'exchange',
        'cal_date',
        'is_open',
        'pretrade_date',
    ]

    def __init__(self):
        self.token = settings.TUSHARE_API_TOKEN
        ts.set_token(self.token)

    def handle(self, *args, **options):
        pro = ts.pro_api()
        try:
            data = pro.trade_cal(fields=','.join(self.fields))
            for index, item in data.iterrows():
                TradeCalendar.objects.update_or_create(defaults=dict(item), exchange=item['exchange'], cal_date=item['cal_date'])
        except Exception as e:
            print('程序出现异常:' + str(e))
