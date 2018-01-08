# -*- coding: utf-8 -*-
# @Time    : 18-1-6 下午9:42
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : management.py


from core import atm
from core.accounts_operations import *
from shopping_mall import shopping_api

# print('>>> 6. 日常消费流水打印')

while True:
    print('欢迎来到ATM终端操作界面'.center(20, '-'))
    print('>>> 1. 办理信用卡')
    print('>>> 2. 账户信息查询')
    print('>>> 3. 转账')
    print('>>> 4. 提现')
    print('>>> 5. 还款')
    print('>>> 6. 临时挂失')
    print('>>> 7. 购物')
    print('>>> 8. 退出', end='\n\n')

    choice = input('>>> 请输入业务代码: ')

    if choice.isdigit():
        if int(choice) == 1:
            print('欢迎开户'.center(20, '-'))
            atm.create_new_accounts()

        elif int(choice) == 2:
            view_account_info()

        elif int(choice) == 3:
            transfer()

        elif int(choice) == 4:
            with_draw()

        elif int(choice) == 5:
            pay_back()

        elif int(choice) == 6:
            disable_credit_card()

        elif int(choice) == 7:
            shopping_api.go_shopping()

        elif int(choice) == 8:
            tips = input('>>> 是否退出ATM(y): ')
            if tips == 'y' or tips == 'yes':
                exit('>>> 退出ATM')
        else:
            print('>>> 输入有误, 请重新输入 ')

    # choice1 = input('>>> 是否退出ATM？(q) ')
    # if choice1 == 'q' or choice == 'quit':
    #     tips = input('>>> 确定退出?(y) ')
    #     if tips == 'y' or tips == 'yes':
    #         exit('>>> 退出ATM')
    # else:
    #     pass







