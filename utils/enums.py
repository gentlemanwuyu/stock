"""
枚举
"""

from utils.constants import SH_ID
from utils.constants import SZ_ID
from utils.constants import CH_ID
from utils.constants import STRONG
from utils.constants import WEAK


class IndexEnum:
    """
    指数的枚举
    """
    NORMALS = [SH_ID, SZ_ID, CH_ID]


class StockEnum:
    """
    股票的枚举
    """
    CONTINUED_DAYS = [3, 5, 10]  # 持续天数
    STRONG_DIRECTIONS = [STRONG, WEAK]
