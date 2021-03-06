from django.db import models


# Create your models here.
class StockDailyAvg(models.Model):
    class Meta:
        db_table = 'stock_daily_avgs'

    ts_code = models.CharField(max_length=255, default='')
    trade_date = models.CharField(max_length=255, default='')
    p5 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 5日平均价格
    p10 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 10日平均价格
    p20 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 20日平均价格
    p30 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 30日平均价格
    p60 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 60日平均价格
    p200 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 200日平均价格
    a5 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 5日平均成交金额
    a10 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 10日平均成交金额
    a20 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 20日平均成交金额
    a30 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 30日平均成交金额
    a60 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 60日平均成交金额
    a200 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 200日平均成交金额
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IndexDailyAvg(models.Model):
    class Meta:
        db_table = 'index_daily_avgs'

    ts_code = models.CharField(max_length=255, default='')
    trade_date = models.CharField(max_length=255, default='')
    p5 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 5日平均价格
    p10 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 10日平均价格
    p20 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 20日平均价格
    p30 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 30日平均价格
    p60 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 60日平均价格
    p200 = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # 200日平均价格
    a5 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 5日平均成交金额
    a10 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 10日平均成交金额
    a20 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 20日平均成交金额
    a30 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 30日平均成交金额
    a60 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 60日平均成交金额
    a200 = models.DecimalField(max_digits=14, decimal_places=4, null=True)  # 200日平均成交金额
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
