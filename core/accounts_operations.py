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
    card_id = account.get('card_id')
    while True:
        withdraw_amount = input('>>> 请输入提款金额: ')
        if withdraw_amount.isdigit():
            withdraw_amount = int(withdraw_amount)
            if int(withdraw_amount)*105/100 + account['pay_bills'] <= (account['balance'] + account['available_credit']):
                if withdraw_amount < account['balance']:
                    account['balance'] -= withdraw_amount*105/100
                else:
                    account['pay_bills'] = withdraw_amount*105/100 - account['balance'] + account['pay_bills']
                    account['balance'] = 0

                print('>>> 请取走现金，共计 %s 元' % withdraw_amount)
                print('>>> 完成提现完成:账户余额 %s 元, 待还款 %s 元' % (account['balance'], account['pay_bills']), end='\n\n')
                with open(DATABASE.get('path') + '/%s.json' % card_id, 'w') as f:
                    json.dump(account, f)

                choice = input('>>> 是否继续提现？(y)')
                if choice == 'y' or choice == 'yes':
                    pass
                else:
                    break

            else:
                print('>>> 账户余额和可用额度不足,不能提现')

        else:
            print('>>> 输入有误，请重新输入')


@login
def pay_back(**kwargs):
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
        choice = input('您的账户余额足够扣款，继续充值？(y)')
        if choice == 'y' or choice == 'yes':
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
    count = 0
    account_backup = {}
    while count < 3:
        input_card_id = input('>>> 请输入您的信用卡账号：　')
        if '%s.json' % input_card_id in os.listdir(DATABASE.get('path')):
            file_name = DATABASE.get('path') + '/%s.json' % input_card_id
            f = open(file_name, 'r')
            account = json.load(f)
            account_backup = account
            password = account.get('password', '')
            while count < 3:
                input_pwd = input('>>> 请输入您的密码：　')
                if input_pwd == password:
                    print('登陆成功'.center(25, '-'))
                    account['lock_status'] = 2
                    with open(DATABASE.get('path') + '/%s.json' % input_card_id, 'w') as f:
                        json.dump(account, f)
                    print('>>> 账号(%s)已经成功挂失' % input_card_id)
                    count = 3
                else:
                    count += 1
        else:
            print('>>> 您输入的信用卡账号不存在，请核对后重新输入')
        count += 1

    else:
        account_backup['lock_status'] = 1
        card_id = account_backup.get('card_id', '')
        with open(DATABASE.get('path') + '/%s.json' % card_id, 'w') as f:
            json.dump(account, f)
        exit('>>> 对不起，　您的密码输入次数过多，已被锁定')


@login
def checkout(**kwargs):
    payment_amount = float(kwargs.get('payment_amount', 0))
    account = kwargs.get('account')
    pay_bills = account.get('pay_bills')
    balance = account.get('balance')
    available_credit = account.get('available_credit')
    card_id = account.get('card_id', '')
    if payment_amount > available_credit - pay_bills + balance:
        min_need_money = payment_amount - available_credit + pay_bills - balance
        print('>>> 对不起，您的账户余额不足, 需至少充值%s 元' % min_need_money)

        choice = input('>>> 是否充值?(y) ')
        if choice == 'y' or choice == 'yes':
            while True:
                charge_money = input('>>> 请输入您要充值的金额: ')
                if charge_money.isdigit():
                    charge_money = float(charge_money)
                    if charge_money >= min_need_money:
                        account['balance'] = charge_money - min_need_money
                        with open(DATABASE.get('path') + '/%s.json' % account['card_id'], 'w') as f:
                            json.dump(account, f)
                        print('>>> 付款成功,消费 %s 元' % payment_amount)
                        print('>>> 您当前账户余额为(%s)元, 欠款 %s 元' % (account['balance'], account['pay_bills']))
                        choice = input('>>> 退出购物? (q) ')
                        if choice == 'q' or choice == 'quit':
                            tips = input('>>> 确定退出购物? (y) ')
                            if tips == 'y' or tips == 'yes':
                                print('>>> 欢迎下次再来!')
                                break
                        else:
                            break
                    else:
                        print('>>> 充值金额不够，请重新输入')

                else:
                    print('>>> 金额输入有误')

        else:
            pass

    else:

        if payment_amount < balance:
            account['balance'] = balance - payment_amount
        else:
            account['balance'] = 0
            account['pay_bills'] = pay_bills + payment_amount - balance

        print('>>> 付款成功,消费 %s 元' % payment_amount)
        print('>>> 您当前账户余额为(%s)元, 欠款 %s 元'%(account['balance'], account['pay_bills']))
        with open(DATABASE.get('path') + '/%s.json' % account['card_id'], 'w') as f:
            json.dump(account, f)

        choice = input('>>> 退出购物? (q) ')
        if choice == 'q' or choice == 'quit':
            tips = input('>>> 确定退出? (y) ')
            if tips == 'y' or tips == 'yes':
                print('>>> 欢迎下次再来!')

