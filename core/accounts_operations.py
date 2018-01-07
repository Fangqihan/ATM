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
    print('>>> 账户余额 %s 元, 待还款 %s 元' % (account['balance'], account['pay_bills']), end='\n\n')


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

    if pay_bills > balance:
        print('>>> 账户余额不足还款，需至少充值: %s 元' % (pay_bills - balance))

        while True:
            pay_amount = int(input('>>> 请输入充值金额: '))
            if pay_amount < (pay_bills - balance):
                print('>>> 余额不足还款, 请重新充值足够的金额!')

            else:
                account['balance'] = balance + pay_amount - pay_bills
                account['pay_bills'] = 0
                break

    else:
        pay_amount = int(input('>>> 请输入充值金额: '))
        account['balance'] = balance - pay_bills + pay_amount
        account['pay_bills'] = 0

    print('>>> 还款完成:账户余额 %s 元, 待还款 %s 元' % (account['balance'], account['pay_bills']), end='\n\n')
    with open(DATABASE.get('path') + '/%s.json' % card_id, 'w') as f3:
        json.dump(account, f3)


@login
def transfer(*args, **kwargs):
    account = kwargs.get('account')
    pay_bills = account.get('pay_bills')
    balance = account.get('balance')
    available_credit = account.get('available_credit')

    while True:
        to_card_id = input('>>> 请输入对方账号: ')

        if '%s.json' % to_card_id in os.listdir(DATABASE.get('path')):
            transfer_amount = input('>>> 请输入汇款金额: ')

            if transfer_amount.isdigit():
                transfer_amount = int(transfer_amount)

                if transfer_amount >= available_credit - pay_bills + balance:
                    print('>>> 对不起，您的账户余额不足, 请重新输入')

                else:
                    f_to = open(DATABASE.get('path') + '/%s.json' % to_card_id, 'r')
                    to_account = json.load(f_to)

                    if transfer_amount < balance:
                        account['balance'] = balance - transfer_amount

                    else:
                        account['balance'] = 0
                        account['pay_bills'] = pay_bills + transfer_amount - balance

                    to_account['balance'] = to_account['balance'] + transfer_amount
                    print('>>> 转账成功,向卡号(%s)转账 %s 元'%(to_account['card_id'], transfer_amount))
                    print('>>> 您当前账户余额为(%s)元, 欠款 %s 元'%(account['balance'], account['pay_bills']))

                    with open(DATABASE.get('path') + '/%s.json' % to_card_id, 'w') as f_to1:
                        json.dump(to_account, f_to1)
                    with open(DATABASE.get('path') + '/%s.json' % account['card_id'], 'w') as f:
                        json.dump(account, f)

                    choice = input('>>> 继续转账?(y)')
                    if choice == 'yes' or choice == 'y':
                        pass
                    else:
                        break

            else:
                print('>>> 金额输入有误，请重新输入')

        else:
            print('>>> 您输入的转账号码有误， 请重新输入')



def disable_credit_card(*args, **kwargs):
    pass
