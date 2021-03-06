# -*- coding: utf-8 -*-
# @Time    : 18-1-7 下午9:30
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : login_api.py


import datetime
import json
import os

from conf.settings import DATABASE
from core import atm
from core.logger import log_generate

LOGIN_STATUS = 0
ACCOUNT = {}


def login(func):

    def inner(**kwargs):
        global LOGIN_STATUS
        global ACCOUNT
        print('=========================')
        payment_amount = kwargs.get('payment_amount', 0)
        if LOGIN_STATUS:
            return func(account=ACCOUNT, payment_amount=payment_amount)

        print('\n'+'登录中'.center(30, '-'))
        count = 0
        while count < 3:
            credit_code = input('>>> 请输入您的信用卡卡号: ')
            # 判断输入的卡号是否开户
            if '%s.json' % credit_code not in os.listdir(DATABASE.get('path')):
                print('\033[1;35m 此信用卡账号没有开户记录 \033[0m')
                count += 1

            else:
                # 根据卡号获取用户信息文件
                f = open(DATABASE.get('path')+'/%s.json'%credit_code, 'r')
                account = json.load(f)
                card_id = account.get('card_id', '')
                ACCOUNT = account
                account_password = account.get('password')

                lock_status = account.get('lock_status')
                # 判断当前用户是否冻结
                if lock_status == 1:
                    print('\033[1;31m 对不起, 您的账户已被锁定, 请前往银行柜台解锁! \033[0m', end='\n\n')
                    logout()
                    break

                # 信用卡过期
                elif lock_status == 2:
                    choice = input('>>>\033[1;35m 对不起, 您的信用卡已被过期,是否重新办理?(y) \033[0m : ')
                    if choice == 'y' or choice == 'yes':
                        atm.create_new_accounts()

                # 正常
                elif lock_status == 0:
                    while count < 3:
                        password = input('>>> 请输入您的密码: ')
                        if password != account_password:
                            count += 1
                        else:
                            log_generate(log_type='access', card_id=card_id, message='login')
                            print('\n' + '登录成功'.center(30, '-'))

                            LOGIN_STATUS = 1
                            count = 3

                            day = datetime.date.today().day
                            expire_date_str = account.get('expire_date')
                            expire_date = datetime.datetime.strptime(expire_date_str, '%Y-%m-%d').date()

                            # 判断信用卡是否过期
                            if datetime.date.today() > expire_date:
                                account['lock_status'] = 2
                                with open(DATABASE.get('path') + '/%s.json' % credit_code, 'w') as f2:
                                    json.dump(account, f2)
                                exit('>>> \033[1;35m 对不起,您的信用卡已经过期,请重新办理\033[0m')

                            pay_day = int(account.get('pay_day'))

                            # 若当前用户信息正常则携带相关的用户信息返回
                            if datetime.date.today().day < pay_day:
                                return func(account=account, day=day, payment_amount=payment_amount)

                            print('>>> \033[1;31m 系统检测到您的信用卡已超过最迟还款期限，开始进行自动扣款 \033[0m')
                            return atm.pay_back_urgently(account=account)

                    count = 3

        # 账户冻结
        ACCOUNT['lock_status'] = 1
        card_id = ACCOUNT.get('card_id', '')
        with open(DATABASE.get('path') + '/%s.json' % card_id, 'w') as f:
            json.dump(account, f)
        exit('>>> \033[1;35m 对不起，您的密码输入次数过多，已被锁定 \033[0m')

    return inner


def logout(**kwargs):
    global LOGIN_STATUS
    if kwargs:
        LOGIN_STATUS = kwargs.get('LOGIN_STATUS')
    if LOGIN_STATUS == 1:
        tips = input('>>> 退出本账号?\033[1;35m (q)\033[0m: ')
        if tips == 'q' or tips == 'quit':
            LOGIN_STATUS = 0
            log_generate(log_type='access', card_id=ACCOUNT['card_id'], message='logout')
            choice = input('>>> 确定退出ATM?\033[1;35m (q)\033[0m:')
            if choice == 'q' or choice == 'quit':
                exit('>>> 欢迎下次光临！')
    else:
        choice = input('>>> 确定退出ATM?\033[1;35m (q)\033[0m:')
        if choice == 'q' or choice == 'quit':
            exit('>>> 欢迎下次光临！')


def check_login():
    if LOGIN_STATUS == 0:
        return False
    return True


