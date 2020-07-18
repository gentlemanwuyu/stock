"""
自定义函数
"""


def make_cache_key(key, key_prefix, version):
    """
    缓存键值的生成方法
    :param key:
    :param key_prefix:
    :param version:
    :return:
    """
    return ':'.join([key_prefix, key])
