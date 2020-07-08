# Generated by Django 2.1.4 on 2020-06-23 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IndexDailyAvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(default='', max_length=255)),
                ('trade_date', models.CharField(default='', max_length=255)),
                ('p5', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p10', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p20', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p30', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p60', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p200', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('a5', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a10', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a20', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a30', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a60', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a200', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'index_daily_avgs',
            },
        ),
        migrations.CreateModel(
            name='StockDailyAvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(default='', max_length=255)),
                ('trade_date', models.CharField(default='', max_length=255)),
                ('p5', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p10', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p20', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p30', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p60', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('p200', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('a5', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a10', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a20', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a30', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a60', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('a200', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'stock_daily_avgs',
            },
        ),
    ]