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

LOGIN_STATUS = 0
ACCOUNT = {}


def login(func, *args):

    def inner():
        global LOGIN_STATUS
        global ACCOUNT
        if LOGIN_STATUS == 0:

            print('登录中'.center(25, '-'))
            credit_code = input('>>> 请输入您的信用卡卡号: ')
            if '%s.json'%credit_code in os.listdir(DATABASE.get('path')):
                f = open(DATABASE.get('path')+'/%s.json'%credit_code, 'r')
                account = json.load(f)
                ACCOUNT = account
                account_password = account.get('password')
                lock_status = account.get('lock_status')
                if lock_status == 0:
                    count = 0
                    while count < 3:
                        password = input('>>> 请输入您的密码: ')

                        if password == account_password:
                            print('\n'+'登录成功'.center(25, '-'))
                            LOGIN_STATUS = 1
                            count = 3
                            day = datetime.date.today().day
                            expire_date_str = account.get('expire_date')
                            expire_date = datetime.datetime.strptime(expire_date_str, '%Y-%m-%d').date()

                            if datetime.date.today() > expire_date:
                                account['lock_status'] = 2
                                with open(DATABASE.get('path')+'/%s.json'%credit_code, 'w') as f2:
                                    json.dump(account, f2)
                                exit('>>> 对不起,您的信用卡已经过期,请重新办理')

                            else:
                                pay_day = int(account.get('pay_day'))

                                if datetime.date.today().day >= pay_day:
                                    return atm.pay_back_without_login(account=account)

                                else:
                                    return func(account=account, day=day)

                        else:
                            count += 1
                    else:
                        account['lock_status'] = 1
                        with open(DATABASE.get('path') + '/%s.json' % credit_code, 'w') as f1:
                            json.dump(account, f1)

                elif lock_status == 1:
                    exit('>>> 对不起, 您的账户已被锁定, 请前往银行柜台解锁!')

                elif lock_status == 2:
                    choice = input('>>> 对不起, 您的信用卡已过期,是否重新办理?(y)')
                    atm.create_new_accounts()
                else:
                    pass
            else:
                print('此信用卡账号没有开户记录')

        else:
            return func(account=ACCOUNT)

    return inner



