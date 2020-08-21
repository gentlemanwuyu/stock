from django.db import models


# Create your models here.

class Stock(models.Model):
    class Meta:
        db_table = 'stocks'

    ts_code = models.CharField(max_length=255, default='', unique=True)
    symbol = models.CharField(max_length=255, default='', db_index=True)
    name = models.CharField(max_length=255, default='', db_index=True)
    area = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    fullname = models.CharField(max_length=255, default='')
    enname = models.CharField(max_length=255, default='')
    market = models.CharField(max_length=255, default='')
    exchange = models.CharField(max_length=255, default='')
    curr_type = models.CharField(max_length=255, default='')
    list_status = models.CharField(max_length=255, default='')
    list_date = models.CharField(max_length=255, default='')
    delist_date = models.CharField(max_length=255, null=True)
    is_hs = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StockDailyData(models.Model):
    class Meta:
        db_table = 'stock_daily_data'
        unique_together = ('ts_code', 'trade_date')

    ts_code = models.CharField(max_length=255, default='')
    trade_date = models.CharField(max_length=255, default='')
    open = models.DecimalField(max_digits=8, decimal_places=2)
    high = models.DecimalField(max_digits=8, decimal_places=2)
    low = models.DecimalField(max_digits=8, decimal_places=2)
    close = models.DecimalField(max_digits=8, decimal_places=2)
    pre_close = models.DecimalField(max_digits=8, decimal_places=2)
    change = models.DecimalField(max_digits=8, decimal_places=2)
    pct_chg = models.DecimalField(max_digits=8, decimal_places=4)
    vol = models.DecimalField(max_digits=14, decimal_places=4)
    amount = models.DecimalField(max_digits=14, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Index(models.Model):
    class Meta:
        db_table = 'indexes'

    ts_code = models.CharField(max_length=255, default='', unique=True)
    name = models.CharField(max_length=255, default='', db_index=True)
    fullname = models.CharField(max_length=255, null=True)
    market = models.CharField(max_length=255, null=True)
    publisher = models.CharField(max_length=255, null=True)
    index_type = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    base_date = models.CharField(max_length=255, null=True)
    base_point = models.DecimalField(max_digits=12, decimal_places=2)
    list_date = models.CharField(max_length=255, null=True)
    weight_rule = models.CharField(max_length=255, null=True)
    desc = models.TextField(null=True)
    exp_date = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IndexDailyData(models.Model):
    class Meta:
        db_table = 'index_daily_data'
        unique_together = ('ts_code', 'trade_date')

    ts_code = models.CharField(max_length=255, default='')
    trade_date = models.CharField(max_length=255, default='')
    open = models.DecimalField(max_digits=8, decimal_places=2)
    high = models.DecimalField(max_digits=8, decimal_places=2)
    low = models.DecimalField(max_digits=8, decimal_places=2)
    close = models.DecimalField(max_digits=8, decimal_places=2)
    pre_close = models.DecimalField(max_digits=8, decimal_places=2)
    change = models.DecimalField(max_digits=8, decimal_places=2)
    pct_chg = models.DecimalField(max_digits=8, decimal_places=4)
    vol = models.DecimalField(max_digits=14, decimal_places=4)
    amount = models.DecimalField(max_digits=14, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TradeCalendar(models.Model):
    class Meta:
        db_table = 'trade_calendars'
        unique_together = ('exchange', 'cal_date')

    exchange = models.CharField(max_length=255, default='')
    cal_date = models.CharField(max_length=255, default='')
    pretrade_date = models.CharField(max_length=255, null=True)
    is_open = models.IntegerField(null=True)


class StockName(models.Model):
    class Meta:
        db_table = 'stock_names'
        unique_together = ('ts_code', 'start_date')

    ts_code = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, null=True)
    start_date = models.CharField(max_length=255, null=True)
    end_date = models.CharField(max_length=255, null=True)
    ann_date = models.CharField(max_length=255, null=True)
    change_reason = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
