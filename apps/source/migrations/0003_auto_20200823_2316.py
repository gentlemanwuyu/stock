# Generated by Django 2.1.4 on 2020-08-23 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0002_auto_20200820_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(default='', max_length=255)),
                ('ann_date', models.CharField(max_length=255, null=True)),
                ('f_ann_date', models.CharField(max_length=255, null=True)),
                ('end_date', models.CharField(default='', max_length=255)),
                ('report_type', models.IntegerField(null=True)),
                ('comp_type', models.IntegerField(null=True)),
                ('basic_eps', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('diluted_eps', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('total_revenue', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('revenue', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('int_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('prem_earned', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('comm_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('n_commis_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('n_oth_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('n_oth_b_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('prem_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('out_prem', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('une_prem_reser', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('reins_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('n_sec_tb_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('n_sec_uw_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('n_asset_mg_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('oth_b_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('fv_value_chg_gain', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('invest_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('ass_invest_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('forex_gain', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('total_cogs', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('oper_cost', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('int_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('comm_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('biz_tax_surchg', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('sell_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('admin_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('fin_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('assets_impair_loss', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('prem_refund', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('compens_payout', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('reser_insur_liab', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('div_payt', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('reins_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('oper_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('compens_payout_refu', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('insur_reser_refu', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('reins_cost_refund', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('other_bus_cost', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('operate_profit', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('non_oper_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('non_oper_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('nca_disploss', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('total_profit', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('income_tax', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('n_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('n_income_attr_p', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('minority_gain', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('oth_compr_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('t_compr_income', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('compr_inc_attr_p', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('compr_inc_attr_m_s', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('ebit', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('ebitda', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('insurance_exp', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('undist_profit', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('distable_profit', models.DecimalField(decimal_places=4, max_digits=18, null=True)),
                ('update_flag', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'stock_incomes',
            },
        ),
        migrations.AlterUniqueTogether(
            name='stockincome',
            unique_together={('ts_code', 'end_date')},
        ),
    ]