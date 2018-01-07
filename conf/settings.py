# -*- coding: utf-8 -*-
# @Time    : 18-1-7 上午9:47
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : settings.py


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


DATABASE = {
    'engine': 'file_storage', #support mysql,postgresql in the future
    'name':'accounts_db',
    'path': "%s/accounts_db" % BASE_DIR
}