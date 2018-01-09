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
    card_id = kwargs.get('card_id')

    if log_type == 'access':
        message = kwargs.get('message', '')
        file_name = LOG_TYPES['access']
        logger = logging.getLogger(card_id)
        logger.setLevel(level=logging.INFO)

        file_handler = logging.FileHandler(LOG_PATH+file_name)
        logger.addHandler(file_handler)

        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        file_handler.setFormatter(file_formatter)

        logger.info(message)
        logger.removeHandler(file_handler)

    elif log_type == 'transaction':
        message = kwargs.get('message', {})
        message = ' '.join([message['type'], '￥'+str(message['amount']), message['info']])

        file_name = LOG_TYPES['transaction']
        logger = logging.getLogger(card_id)
        logger.setLevel(level=logging.INFO)

        file_handler = logging.FileHandler(LOG_PATH + file_name)
        logger.addHandler(file_handler)

        file_formater = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        file_handler.setFormatter(file_formater)

        logger.info(message)
        logger.removeHandler(file_handler)






