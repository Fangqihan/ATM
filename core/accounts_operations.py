# -*- coding: utf-8 -*-
# @Time    : 18-1-7 上午9:26
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : accounts_db.py.py
# 用于从文件里加载和存储账户数据

import json
import datetime

from core.auth import login, logout
from conf.settings import *
from core.logger import log_generate


@login
def view_account_info(*args, **kwargs):
    account = kwargs.get('account', '')
    balance = account.get('balance')
    pay_bills = account.get('pay_bills')
    print('>>> 账户余额 %s 元, 待还款 %s 元' % (balance, pay_bills), end='\n')
    tips = input('>>> 回到主页面\n')


@login
def with_draw(*args, **kwargs):
    account = kwargs.get('account')
    card_id = account.get('card_id')
    while True:
        withdraw_amount = input('>>> 请输入提款金额: ')
        if withdraw_amount.isdigit():
            withdraw_amount = int(withdraw_amount)
            if withdraw_amount * 105/100 + account['pay_bills'] <= (account['balance'] + account['available_credit']):
                if withdraw_amount < account['balance']:
                    account['balance'] -= withdraw_amount*105/100
                    log_generate(log_type='transaction', card_id=card_id,
                                 message={'type': 'withdraw', 'amount': -withdraw_amount, 'info': 'from_balance'})
                else:
                    account['pay_bills'] = withdraw_amount*105/100 - account['balance'] + account['pay_bills']
                    account['balance'] = 0
                    log_generate(log_type='transaction', card_id=card_id,
                                 message={'type': 'withdraw', 'amount': -withdraw_amount, 'info': 'from_pay_bills'})

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
    if pay_bills > 0:
        if pay_bills > balance:
            print('>>> 账户余额不足还款，需至少充值: %s 元' % (pay_bills - balance))
            while True:
                pay_amount = int(input('>>> 请输入充值金额: '))
                if pay_amount < (pay_bills - balance):
                    print('>>> 充值失败,请至少充值%s元!' % (pay_bills - balance))

                else:
                    account['balance'] = balance + pay_amount - pay_bills
                    account['pay_bills'] = 0
                    log_generate(log_type='transaction', card_id=card_id,message={'type': 'charge', 'amount': str(pay_amount), 'info': ''})
                    log_generate(log_type='transaction', card_id=card_id,message={'type': 'pay_back', 'amount': str(pay_bills), 'info': ''})
                    print('>>> 还款完成:账户余额 %s 元, 待还款 %s 元' % (account['balance'], account['pay_bills']), end='\n\n')
                    break

        else:
            log_generate(log_type='transaction', card_id=card_id,
                         message={'type': 'pay_back', 'amount': str(pay_bills), 'info': ''})
            account['balance'] = balance - pay_bills
            account['pay_bills'] = 0
            print('>>> 还款完成:账户余额 %s 元, 待还款 %s 元' % (account['balance'], account['pay_bills']), end='\n\n')

    else:
        choice = input('>>> 扣款完成，继续充值？（y）')
        if choice == 'y' or choice == 'yes':
            pay_amount = int(input('>>> 请输入充值金额: '))
            log_generate(log_type='transaction', card_id=card_id,
                         message={'type': 'charge', 'amount': pay_amount, 'info': ''})
            account['balance'] += pay_amount

    with open(DATABASE.get('path') + '/%s.json' % card_id, 'w') as f3:
        json.dump(account, f3)


@login
def transfer(*args, **kwargs):
    account = kwargs.get('account')
    pay_bills = account.get('pay_bills')
    balance = account.get('balance')
    available_credit = account.get('available_credit')
    card_id = account.get('card_id', '')
    while True:
        to_card_id = input('>>> 请输入对方账号: ')

        if '%s.json' % to_card_id in os.listdir(DATABASE.get('path')):
            if to_card_id != card_id:
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
                        log_generate(log_type='transaction', card_id=card_id,
                                     message={'type': 'transfer', 'amount': transfer_amount, 'info': 'to_'+to_card_id})
                        log_generate(log_type='transaction', card_id=to_card_id,
                                     message={'type': 'receive', 'amount': transfer_amount, 'info': 'from_'+card_id})
                        print('\n'+'>>> 转账成功,向卡号(%s)转账 %s 元'%(to_account['card_id'], transfer_amount))
                        print('>>> 您当前账户余额为(%s)元, 欠款 %s 元'%(account['balance'], account['pay_bills']))

                        with open(DATABASE.get('path') + '/%s.json' % to_card_id, 'w') as f_to1:
                            json.dump(to_account, f_to1)
                        with open(DATABASE.get('path') + '/%s.json' % account['card_id'], 'w') as f:
                            json.dump(account, f)

                        choice = input('>>> 继续转账?(y)')
                        print()
                        if choice == 'yes' or choice == 'y':
                            pass
                        else:
                            break

                else:
                    print('>>> 金额输入有误，请重新输入')
            else:
                print('>>> 不能给自身账号充值, 请重新输入！')
        else:
            print('>>> 您输入的转账号码有误， 请重新输入')


@login
def disable_credit_card(*args, **kwargs):
    account = kwargs.get('account')
    choice = input('继续锁定该账号?(\033[1;35m (y)\033[0m): ')
    if choice == 'y' or choice == 'yes':
        account['lock_status'] = 1
        card_id = account.get('card_id', '')
        with open(DATABASE.get('path') + '/%s.json' % card_id, 'w') as f:
            json.dump(account, f)
        log_generate(log_type='access', card_id=card_id, message='locked')
        logout()


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

        choice = input('>>> 是否充值?\033[1;35m (y)\033[0m: ')
        if choice == 'y' or choice == 'yes':
            while True:
                charge_money = input('>>> 请输入您要充值的金额: ')
                if charge_money.isdigit():
                    charge_money = float(charge_money)
                    if charge_money >= min_need_money:
                        account['balance'] = charge_money - min_need_money
                        with open(DATABASE.get('path') + '/%s.json' % account['card_id'], 'w') as f:
                            json.dump(account, f)
                        log_generate(log_type='transaction', card_id=card_id,
                                     message={'type': 'charge', 'amount': charge_money, 'info':''})
                        log_generate(log_type='transaction', card_id=card_id,
                                     message={'type': 'consume', 'amount': payment_amount, 'info':''})

                        input('>>> 付款成功,消费 %s 元' % payment_amount)
                        print('>>> 您当前账户余额为(%s)元, 欠款 %s 元' % (account['balance'], account['pay_bills']))

                        choice = input('>>> 退出购物?\033[1;35m  (q) \033[0m ')
                        if choice == 'q' or choice == 'quit':
                            tips = input('>>> 确定退出购物?\033[1;35m (q)\033[0m ')
                            if tips == 'q' or tips == 'quit':
                                print('>>> 欢迎下次再来!')
                                break
                        else:
                            break

                    else:
                        print('>>> 充值金额不够，请重新输入')
                else:
                    print('>>> 金额输入有误 ')

    else:

        if payment_amount < balance:
            account['balance'] = balance - payment_amount
        else:
            account['balance'] = 0
            account['pay_bills'] = pay_bills + payment_amount - balance
        log_generate(log_type='transaction', card_id=card_id, message={'type': 'consume', 'amount': payment_amount, 'info':''})

        input('>>> 付款成功,消费 %s 元, 任意键继续' % payment_amount)
        print('>>> 您当前账户余额为(%s)元, 欠款 %s 元'%(account['balance'], account['pay_bills']))
        with open(DATABASE.get('path') + '/%s.json' % account['card_id'], 'w') as f:
            json.dump(account, f)


@login
def output_transaction_records(**kwargs):
    account = kwargs.get('account')
    card_id = account.get('card_id', '')
    created_date_original = ''
    search_result = []
    # 找到账户对应的创建时间
    f = open(LOG_PATH + LOG_TYPES['access'], 'r')
    for line in f:
        line.strip()
        line = line.split()
        # print(line)
        if line[-2] == card_id and line[-1] == 'create_account':
            created_date_original = line[0]
            break

    if created_date_original:
        created_date = datetime.datetime.strptime(created_date_original, '%Y-%m-%d')
        created_date = datetime.date(year=created_date.year, month=created_date.month, day=1)  # 转换成date类型,仅仅比较年月
        present_date = datetime.date.today()
        present_date = datetime.date(year=present_date.year, month=present_date.month, day=1)
        print('开始查询月度消费记录'.center(20, '-'))
        while True:
            year_str = input('>>> 请输入年: ')
            month_str = input('>>> 请输入月份：　')

            if year_str.isdigit() and month_str.isdigit():

                if isinstance(eval(year_str), int) and isinstance(eval(month_str), int) and eval(year_str) in range(1970,
                                                                                                                    2050) and eval(
                        month_str) in range(1, 13):
                    search_date = datetime.date(year=int(year_str), month=int(month_str), day=1)
                    if created_date <= search_date and present_date >= search_date:
                        f1 = open(LOG_PATH + LOG_TYPES['transaction'], 'r')
                        for line in f1:
                            line.strip()
                            line = line.split()
                            date_lst = line[0].split('-')
                            if int(date_lst[0]) == int(year_str) and int(date_lst[1]) == int(month_str):
                                if line[3] == card_id:
                                    search_result.append(line)
                        search_result = [' '.join(i) for i in search_result]
                        for i in search_result:
                            print(i, end='\n')
                        choice = input('>>> 退出查询(q): ')
                        if choice == 'q' or choice == 'quit':
                            break

                    else:
                        print('查询日期有误,请重新输入, 必须在注册日期%s之后' % str(created_date_original))

                else:
                    print('>>> 日期有误,请重新输入')

            else:
                print('>>> 日期有误,请重新输入')


    else:
        print('>>> 对不起,该账号创建时间不详,无法对齐进行查询')




















