from datetime import datetime
from django_redis import get_redis_connection
from django.conf import settings
from apps.source.models import TradeCalendar
from apps.source.models import Stock
from utils.constants import STRONG
import logging


class GetContinuedStrongList:
    days = 3
    start_date = None
    direction = STRONG
    redis_list_base_name = None

    def __init__(self, params):
        self.logger = logging.getLogger('log')
        self.redis_conn = get_redis_connection('default')  # redis连接
        # redis 列表基础名
        self.redis_list_base_name = settings.CACHES['default']['KEY_PREFIX'] + ':continued_stock:'
        if 'days' in params.keys():
            self.days = int(params['days'])
        if 'start_date' in params.keys():
            self.start_date = datetime.strptime(params['start_date'], '%Y-%m-%d').strftime('%Y%m%d')
        if 'status' in params.keys():
            self.direction = params['status']

    def handle(self):
        self.init_params()
        redis_key = self.redis_list_base_name + self.start_date + '_' + self.direction + '_' + str(self.days)
        ts_codes = self.redis_conn.lrange(redis_key, 0, -1)
        if not ts_codes.__len__():
            return []
        ts_codes = [item.decode('utf-8') for item in ts_codes]
        stocks = Stock.objects.filter(ts_code__in=ts_codes).values('ts_code', 'name').all()
        return list(stocks)

    def init_params(self):
        # 计算起始日期
        if not self.start_date:
            today = datetime.now().strftime('%Y%m%d')
            self.start_date = TradeCalendar.objects.filter(cal_date__lte=today, is_open=1).order_by('-id').values_list(
                'cal_date').first()[0]
