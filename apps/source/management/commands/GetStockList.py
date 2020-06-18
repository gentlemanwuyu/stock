# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from apps.source.models import Stock
import tushare as ts


class Command(BaseCommand):
    help = '获取股票列表'
    fields = [
        'ts_code',
        'symbol',
        'name',
        'area',
        'industry',
        'fullname',
        'enname',
        'market',
        'exchange',
        'curr_type',
        'list_status',
        'list_date',
        'delist_date',
        'is_hs',
    ]

    def __init__(self):
        self.token = settings.TUSHARE_API_TOKEN

    def handle(self, *args, **options):
        ts.set_token(self.token)
        pro = ts.pro_api()

        try:
            data = pro.stock_basic(list_status='L', fields=','.join(self.fields))
            for index, item in data.iterrows():
                Stock.objects.update_or_create(defaults=dict(item), ts_code=item['ts_code'])
        except Exception as e:
            print('程序出现异常:' + str(e))
