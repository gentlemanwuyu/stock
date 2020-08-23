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


class StockIncome(models.Model):
    class Meta:
        db_table = 'stock_incomes'
        unique_together = ('ts_code', 'end_date')

    ts_code = models.CharField(max_length=255, default='')  # TS代码
    ann_date = models.CharField(max_length=255, null=True)  # 公告日期
    f_ann_date = models.CharField(max_length=255, null=True)  # 实际公告日期
    end_date = models.CharField(max_length=255, default='')  # 报告期
    report_type = models.IntegerField(null=True)  # 报告类型
    comp_type = models.IntegerField(null=True)  # 公司类型
    basic_eps = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 基本每股收益
    diluted_eps = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 稀释每股收益
    total_revenue = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 营业总收入
    revenue = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 营业收入
    int_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 利息收入
    prem_earned = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 已赚保费
    comm_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 手续费及佣金收入
    n_commis_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 手续费及佣金净收入
    n_oth_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 其他经营净收益
    n_oth_b_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 加:其他业务净收益
    prem_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 保险业务收入
    out_prem = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:分出保费
    une_prem_reser = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 提取未到期责任准备金
    reins_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 其中:分保费收入
    n_sec_tb_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 代理买卖证券业务净收入
    n_sec_uw_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 证券承销业务净收入
    n_asset_mg_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 受托客户资产管理业务净收入
    oth_b_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 其他业务收入
    fv_value_chg_gain = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 加:公允价值变动净收益
    invest_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 加:投资净收益
    ass_invest_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 其中:对联营企业和合营企业的投资收益
    forex_gain = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 加:汇兑净收益
    total_cogs = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 营业总成本
    oper_cost = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:营业成本
    int_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:利息支出
    comm_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:手续费及佣金支出
    biz_tax_surchg = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:营业税金及附加
    sell_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:销售费用
    admin_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:管理费用
    fin_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:财务费用
    assets_impair_loss = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:资产减值损失
    prem_refund = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 退保金
    compens_payout = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 赔付总支出
    reser_insur_liab = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 提取保险责任准备金
    div_payt = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 保户红利支出
    reins_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 分保费用
    oper_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 营业支出
    compens_payout_refu = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:摊回赔付支出
    insur_reser_refu = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:摊回保险责任准备金
    reins_cost_refund = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:摊回分保费用
    other_bus_cost = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 其他业务成本
    operate_profit = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 营业利润
    non_oper_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 加:营业外收入
    non_oper_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 减:营业外支出
    nca_disploss = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 其中:减:非流动资产处置净损失
    total_profit = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 利润总额
    income_tax = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 所得税费用
    n_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 净利润(含少数股东损益)
    n_income_attr_p = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 净利润(不含少数股东损益)
    minority_gain = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 少数股东损益
    oth_compr_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 其他综合收益
    t_compr_income = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 综合收益总额
    compr_inc_attr_p = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 归属于母公司(或股东)的综合收益总额
    compr_inc_attr_m_s = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 归属于少数股东的综合收益总额
    ebit = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 息税前利润
    ebitda = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 息税折旧摊销前利润
    insurance_exp = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 保险业务支出
    undist_profit = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 年初未分配利润
    distable_profit = models.DecimalField(max_digits=18, decimal_places=4, null=True)  # 可分配利润
    update_flag = models.IntegerField(null=True)  # 更新标识，0未修改1更正过
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
