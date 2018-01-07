# -*- coding: utf-8 -*-
# @Time    : 18-1-7 下午9:30
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : shopping_cart_2nd_edition.py.py


'''
项目说明:
目前没有用函数,全程逻辑判断if和while语句,所以难免有重复代码
购物记录数据存储形式:{name: [pwd, salary, shopping_history]}
本程序分为三种情况:
    1.没有缓存文件
    2.有缓存文件
        2.1老用户登录
        2.2新用户注册
'''

import pickle
import os
from collections import deque



GOODS = [
    {"name": "mac_pro", "price": 1999},
    {"name": "mouse", "price": 10},
    {"name": 'book', "price": 70},
    {"name": "iphone", "price": 8888},
    {"name": "bottle", "price": 50},
    {"name": "shoe", "price": 399},
    {"name": "jacket", "price": 500},
]

username = input('您的用户名: ')
shopping_history = deque(maxlen=3)
shopping_cart = []

# 有缓存
if os.path.exists('user_info.txt'):
    USER_INFO = pickle.load(open('user_info.txt', 'rb'))

    # 老用户登录
    if username in USER_INFO.keys():
        n = 0
        while n < 3:  # 三次输入机会
            password = input('您的密码: ')
            n += 1
            if password == USER_INFO[username][0]:
                print('%s, 欢迎您登录'%username)
                salary = USER_INFO[username][1]
                print('您的账户余额: \033[1;31m%d\33[0m' % salary)
                shopping_history = USER_INFO[username][2]

                # 浏览记录提醒
                history_tip = input('是否浏览之前的购买记录?(y|n)')
                if history_tip == 'y' or history_tip == 'yes':
                    print('最近三次的购买清单如下: ')
                    for item in shopping_history:
                        print(item)

                flag = True
                while flag:
                    #提醒用户是否继续购买
                    tip2 = input('退出请输入(q|quit),按任意键继续购物:  ')
                    if tip2 == 'q' or tip2 == 'quit':
                        flag = False
                        n = 3
                    else:
                        #打印商品列表
                        print('商品列表'.center(25, '-'))
                        print('code'.ljust(6), 'name'.ljust(10), 'price'.ljust(10))
                        for i in range(len(GOODS)):
                            print(str(i).ljust(6), GOODS[i]['name'].ljust(10),
                                  str(GOODS[i]['price']).ljust(10))

                        # 用户输入商品编码
                        code = input('请输入商品的编码(0-%s的整数): ' % (len(GOODS)))
                        if code.isdigit(): #判断输入的是否是数字
                            code = int(code)
                            # 判断编码是否超出索引范围
                            if code in range(len(GOODS)):
                                #判断用户余额是否充足
                                if salary - GOODS[code]['price'] > 0:
                                    salary -= GOODS[code].get('price')
                                    shopping_cart.append(GOODS[code].get('name'))  # 将物品装进购物车
                                else:
                                    # 提示余额不足
                                    tip1 = input('对不起,您的余额不足,是否充值?充值请输入y|yes, 按任意键退出购买')
                                    if tip1 == 'y' or tip1 == 'yes':
                                        charge = int(input('请输入你充值的金额(正整数): '))
                                        if type(charge) == int:
                                            if charge > 0:
                                                salary += charge
                                                print('%s,您的账户余额: \033[1;31m%d\33[0m' % (username, salary))
                                    else:
                                        flag = False
                                        n = 3 #退出大循环
                        else:
                            print('此商品不存在,请重新选择!')

                shopping_history.append(shopping_cart)
                print('您本次购买的商品如下: \033[1;31m%s\33[0m' % ','.join(shopping_cart))
                print('您的账户余额: \033[1;31m%d\33[0m' % salary)
                USER_INFO[username] = [password, salary, shopping_history]
                pickle.dump(USER_INFO, open('user_info.txt', 'wb'))

            else:
                print('密码有误, 请重新输入: ')

    # 新用户注册
    else:
        password = input('您的密码:')
        salary = int(input('请输入您的工资: '))
        flag = True
        while flag:
            # 输出商品列表
            print('商品列表'.center(25, '-'))
            print('code'.ljust(6), 'name'.ljust(10), 'price'.ljust(10))
            for i in range(len(GOODS)):
                print(str(i).ljust(6), GOODS[i]['name'].ljust(10),
                      str(GOODS[i]['price']).ljust(10))

            # 用户输入商品编码
            code = input('请输入商品的编码(0-%s的整数): ' % (len(GOODS)))  # 注意转换成int
            if code.isdigit():
                code = int(code)
                # 判断编码是否超出索引范围
                if code in range(len(GOODS)):
                    # 判断余额是否充足
                    if salary - GOODS[code]['price'] > 0:
                        salary -= GOODS[code].get('price')
                        shopping_cart.append(GOODS[code].get('name'))  # 将物品装进购物车
                        tip = input('退出请输入(q|quit),按任意键继续购物:  ')  # 提示是否退出
                        if tip == 'q' or tip == 'quit':
                            flag = False
                    else:
                        # 提示余额不足
                        tip1 = input('对不起,您的余额不足,是否充值?充值请输入y|yes, 按任意键退出购买')
                        if tip1 == 'y' or tip1 == 'yes':
                            charge = int(input('请输入你充值的金额(正整数): '))
                            if type(charge) == int:
                                if charge > 0:
                                    salary += charge
                                    print('%s,您的账户余额: \033[1;31m%d\33[0m' % (username, salary))
                        else:
                            flag = False
                            n = 3  # 退出大循环
                else:
                    print('此商品不存在,请重新选择!')

            else:
                print('此商品不存在,请重新选择!')

        shopping_history.append(shopping_cart)
        print('您本次购买的商品如下: \033[1;31m%s\33[0m' % ','.join(shopping_cart))
        print('您的账户余额: \033[1;31m%d\33[0m' % salary)
        USER_INFO[username] = [password, salary, shopping_history]
        pickle.dump(USER_INFO, open('user_info.txt', 'wb'))

# 没有缓存文件,只有第一次运行时调用
else:
    USER_INFO = {}
    shopping_cart = []
    password = input('您的密码:')
    salary = int(input('请输入您的工资: '))
    flag = True
    while flag:
        # 输出商品列表
        print('商品列表'.center(25, '-'))
        print('code'.ljust(6), 'name'.ljust(10), 'price'.ljust(10))
        for i in range(len(GOODS)):
            print(str(i).ljust(6), GOODS[i]['name'].ljust(10),
                  str(GOODS[i]['price']).ljust(10))

        # 用户输入商品编码
        code = input('请输入商品的编码(0-%s的整数): ' % (len(GOODS)))  # 注意转换成int
        if code.isdigit():
            # 判断编码是否超出索引范围
            code = int(code)
            if code in range(len(GOODS)):
                # 判断余额是否充足
                if salary - GOODS[code]['price'] > 0:
                    salary -= GOODS[code].get('price')
                    shopping_cart.append(GOODS[code].get('name'))  # 将物品装进购物车
                    tip = input('退出请输入(q|quit),按任意键继续购物:  ')  # 提示是否退出
                    if tip == 'q' or tip == 'quit':
                        flag = False
                else:
                    # 提示余额不足
                    tip1 = input('对不起,您的余额不足,是否充值?充值请输入y|yes, 按任意键退出购买')
                    if tip1 == 'y' or tip1 == 'yes':
                        charge = int(input('请输入你充值的金额(正整数): '))
                        if type(charge) == int:
                            if charge > 0:
                                salary += charge
                                print('%s,您的账户余额: \033[1;31m%d\33[0m' % (username, salary))
                    else:
                        flag = False
                        n = 3  # 退出大循环
            else:
                print('此商品不存在,请重新选择!')
        else:
            print('此商品不存在,请重新选择!')

    shopping_history.append(shopping_cart)
    print('您本次购买的商品如下: \033[1;31m%s\33[0m' % ','.join(shopping_cart))
    print('您的账户余额: \033[1;31m%d\33[0m' % salary)

    USER_INFO[username] = [password, salary, shopping_history]
    pickle.dump(USER_INFO, open('user_info.txt', 'wb'))


