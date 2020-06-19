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
