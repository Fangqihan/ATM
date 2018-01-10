# -*- coding: utf-8 -*-
# @Time    : 18-1-7 上午9:47
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : settings.py


import os
import sys
import logging


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

DATABASE = {
    # 'engine': 'file_storage', #support mysql,postgresql in the future
    'name': 'accounts_db',
    'path': "%s/accounts_db" % BASE_DIR
}


DATABASE_MALL = {
    # 'engine': 'file_storage', #support mysql,postgresql in the future
    'name': 'goods_db',
    'path': "%s/shopping_mall/shopping_db" % BASE_DIR
}

LOG_LEVEL = logging.INFO
LOG_PATH = "%s/log/" % BASE_DIR
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

ACCESS_TYPE = ['login', 'logout', 'create_account', 'disable', 'locked']

TRANSACTION_TYPE = ['transfer', 'receive', 'withdraw', 'charge', 'pay_back', 'consume']

