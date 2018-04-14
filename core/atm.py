# -*- coding: utf-8 -*-
# @Time    : 18-1-7 上午9:25
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : atm.py.py

import json
from conf.settings import *
from datetime import date

from core.accounts_operations import pay_back
from core.logger import log_generate
from core.auth import check_login


def create_new_accounts():
    """"""
    login_status = check_login()
    if login_status:
        tip = input('>>> \033[1;34m 对不起，在登录状态下无法开户,请先退出本账号 \033[0m\n')
        return

    flag = 1
    while flag:
        save_path = DATABASE.get('path')
        card_id = input('>>> 请输入您的卡号: ')
        if len(card_id) < 6:
            print('>>> \033[1;34m 卡号不能小于六位 \033[0m\n')

        else:
            if '%s.json' % card_id in os.listdir(save_path):
                print('\033[1;35m 您注册的卡号已经存在,请重新输入 \033[0m'+'\n')

            else:
                while True:
                    password = input('>>> 请输入六位数密码: ')
                    payday = input('>>> 请选择您的还款日: ')
                    if len(password) < 6:
                        print('>>> \033[1;34m 密码输入有误，请重新输入 \033[0m\n')

                    if not payday.isdigit() or int(payday) not in range(16, 30):
                        print('>>> \033[1;34m 还款日期输入有误，请重新输入\n \033[0m')

                    else:
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
                        log_generate(log_type='access', card_id=card_id, message='create_account')
                        print('\033[1;35m 恭喜您,信用卡(%s) 开户成功! \033[0m'%card_id, end='\n\n')
                        f.close()
                        flag = 0
                        break


def pay_back_urgently(account):
    pay_back(account=account)



