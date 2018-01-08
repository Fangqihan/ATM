# -*- coding: utf-8 -*-
# @Time    : 18-1-7 上午9:25
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : atm.py.py

import json
from conf.settings import *
from datetime import date, datetime

from core.accounts_operations import pay_back


def create_new_accounts():
    save_path = DATABASE.get('path')
    card_id = input('>>> 请输入您的卡号: ')
    if '%s.json' % card_id in os.listdir(save_path):
        print('>>> 您注册的卡号已经存在,请重新输入')
    else:
        password = input('>>> 请输入六位数密码: ')
        payday = int(input('>>> 请选择您的还款日: '))
        today = date.today()
        accounts = {
            'card_id': card_id,
            'password': password,
            'lock_status': 0, # 0 = normal, 1 = locked, 2 = disabled
            'login_status': 0, # 0 = not login, 1 = login
            'pay_bills': 0,  # 应还账单金额
            'balance': 0,  # 账户余额
            'available_credit': 15000,  #　初始信用余额,固定不变
            'settlement_day': 2,  # 每月结算日期,生成上个月的账单
            'pay_day': payday,  # 每月最晚还款日
            'created_date': str(date.today()),
            'expire_date': str(date(year=today.year+3, month=today.month, day=today.day)),

        }
        file_name = save_path+'/%s.json'%accounts['card_id']
        f = open(file_name, 'w')
        json.dump(accounts, f)
        print('>>> 恭喜您,信用卡(%s) 开户成功!'%card_id, end='\n\n')
        f.close()


def pay_back_urgently(**kwargs):
    account = kwargs.get('account', '')
    return pay_back(account=account)


    # charge_amount = kwargs.get('charge_amount', '')
    # account = kwargs.get('account', '')
    # credit_code = account.get('card_id', '')
    # pay_bills = account.get('pay_bills', 0)
    # balance = account.get('balance', 0)
    #
    # if balance > pay_bills:
    #     print('>>> 您的账户余额充足，无需还款')
    # else:
    #     print('>>> 您应还账单金额合计: %s 元' % pay_bills)
    #     min_charge_amount = pay_bills - balance
    #     while True:
    #         pay_amount = int(input('>>> 请输入还款金额: '))
    #         if pay_amount < min_charge_amount:
    #             print('>>> 充值不足还款, 请重新充值!')
    #         else:
    #             account['pay_bills'] = 0
    #             account['balance'] = pay_amount - min_charge_amount
    #             with open(DATABASE.get('path') + '/%s.json' % credit_code, 'w') as f3:
    #                 json.dump(account, f3)
    #             print('>>> 充值完成, 账户余额 %s 元' % (pay_amount - min_charge_amount), end='\n\n')
    #             break




