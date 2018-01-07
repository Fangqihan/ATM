# -*- coding: utf-8 -*-
# @Time    : 18-1-7 上午9:26
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : accounts_db.py.py
# 用于从文件里加载和存储账户数据

import json

from core.auth import login
from conf.settings import *



@login
def view_account_info(*args, **kwargs):
    account = kwargs.get('account')
    print('>>> 还款完成:账户余额 %s 元, 待还款 %s 元' % (account['balance'], account['pay_bills']), end='\n\n')


@login
def with_draw(*args, **kwargs):
    account = kwargs.get('account')
    day = account.get('pay_day')
    cash = input('>>> 请输入提款金额: ')
    if account['balance'] - cash > 0:
        account['balance'] -= cash
    else:
        print('>>> 账户可用不足,不能提现')

    print('提现')


@login
def pay_back(*args, **kwargs):
    account = kwargs.get('account')
    pay_bills = account.get('pay_bills')
    balance = account.get('balance')
    card_id = account.get('card_id')
    choice = input('>>> 是否继续充值?(y)')
    if choice == 'y' or choice == 'yes':
        if pay_bills > balance:
            print('>>> 账户余额不足还款，需充值: %s 元' % (pay_bills - balance))
            while True:
                pay_amount = int(input('>>> 请输入充值金额: '))
                if pay_amount < (pay_bills - balance):
                    print('>>> 余额不足还款, 请重新还款!')
                else:
                    account['pay_bills'] = 0
                    account['balance'] = balance + pay_amount - pay_bills
                    break
        else:
            account['balance'] = balance - pay_bills
            account['pay_bills'] = 0

        print('>>> 还款完成:账户余额 %s 元, 待还款 %s 元' % (account['balance'], account['pay_bills']), end='\n\n')
        with open(DATABASE.get('path') + '/%s.json' % card_id, 'w') as f3:
            json.dump(account, f3)
    else:
        pass




@login
def transfer(*args, **kwargs):
    account_info = kwargs.get('account')
    to_card_id = input('>>> 请输入对方账号: ')
    if '%s.json' % to_card_id in os.listdir(DATABASE.get('path')):
        f = open(DATABASE.get('path') + '/%s.json' % credit_code, 'r')
    print('转账')


def disable_credit_card(*args, **kwargs):
    pass
