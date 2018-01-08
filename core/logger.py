# -*- coding: utf-8 -*-
# @Time    : 18-1-8 下午7:56
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : logger.py


import logging
from logging import handlers

from conf.settings import *


def log_generate(**kwargs):
    log_type = kwargs.get('log_type', '')
    message = kwargs.get('message', '')
    card_id = kwargs.get('card_id')

    if log_type == 'access':
        file_name = LOG_TYPES['access']
        logger = logging.getLogger(card_id)
        logger.setLevel(level=logging.INFO)

        file_handler = logging.FileHandler(LOG_PATH+file_name)
        logger.addHandler(file_handler)

        file_formater = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        file_handler.setFormatter(file_formater)

        logger.info(message)

    elif log_type == 'transactions':
        pass




log_generate(card_id='111111', message='login', log_type='access')






