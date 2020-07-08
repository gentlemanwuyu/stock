# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from apps.source.models import Index
import tushare as ts
import math
import logging


class Command(BaseCommand):
    help = '获取指数列表'
    fields = [
        'ts_code',
        'name',
        'fullname',
        'market',
        'publisher',
        'index_type',
        'category',
        'base_date',
        'base_point',
        'list_date',
        'weight_rule',
        'desc',
        'exp_date',
    ]

    def __init__(self):
        self.logger = logging.getLogger('log')
        self.token = settings.TUSHARE_API_TOKEN
        ts.set_token(self.token)

    def handle(self, *args, **options):
        pro = ts.pro_api()

        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetIndexList]脚本开始：')
        try:
            data = pro.index_basic(fields=','.join(self.fields))
            for index, item in data.iterrows():
                if math.isnan(item['base_point']):
                    item['base_point'] = 0.00
                Index.objects.update_or_create(defaults=dict(item), ts_code=item['ts_code'])
        except Exception as e:
            self.log('程序出现异常:' + str(e))
        self.log('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '][GetIndexList]脚本结束。')

    def log(self, msg):
        print(msg)
        self.logger.info(msg)
