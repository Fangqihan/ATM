# -*- coding: utf-8 -*-
# @Time    : 18-1-6 下午9:42
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : management.py

import os
import sys

from core import atm
from core.accounts_operations import *
from core.auth import logout
from shopping_mall import shopping_api


while True:
    print('欢迎来到ATM终端操作界面'.center(30, '-'))
    print('1. 办理信用卡')
    print('2. 账户信息查询')
    print('3. 转账')
    print('4. 提现')
    print('5. 还款|充值')
    print('6. 购物')
    print("7. 打印账户消费记录")
    print('8. 挂失')
    print('9. 退出', end='\n')

    choice = input('\n'+'>>> 请输入业务代码: ')

    if choice.isdigit():
        if int(choice) == 1:
            print('\n'+'欢迎开户'.center(30, '-'))
            atm.create_new_accounts()

        elif int(choice) == 2:
            view_account_info()

        elif int(choice) == 3:
            transfer()

        elif int(choice) == 4:
            with_draw()

        elif int(choice) == 5:
            pay_back()

        elif int(choice) == 8:
            disable_credit_card()

        elif int(choice) == 6:
            shopping_api.go_shopping()

        elif int(choice) == 9:
            logout()

        elif int(choice) == 7:
            output_transaction_records()

        else:
            print('>>> 输入有误, 请重新输入 ')

