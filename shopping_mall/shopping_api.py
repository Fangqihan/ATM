# -*- coding: utf-8 -*-
# @Time    : 18-1-7 下午9:30
# @Author  : QiHanFang
# @Email   : qihanfang@foxmail.com
# @File    : shopping_cart_2nd_edition.py.py
import json
import hashlib
from collections import namedtuple

from conf.settings import *
from core.accounts_operations import checkout

mall_login_status = 0
goods = {}

def is_superuser(func):
    def inner():
        global mall_login_status

        if mall_login_status == 0:
            save_path = DATABASE_MALL.get('path')
            with open(save_path+'/super_user.json', 'r') as f:
                super_user_info = json.load(f)
                username = super_user_info.get('username', '')
                password = super_user_info.get('password', '')
                count = 0
                while count < 3:
                    md_5 = hashlib.md5()
                    input_username = input('>>> 请输入您的账号：　')
                    input_pwd = input('>>> 请输入您的密码：　')

                    md_5.update(input_username.encode('utf8'))
                    input_username = md_5.hexdigest()
                    md_5.update(input_pwd.encode('utf8'))
                    input_pwd = md_5.hexdigest()

                    if input_username == username and input_pwd == password:
                        mall_login_status = 1
                        goods_db_path = DATABASE_MALL.get('path')
                        with open(goods_db_path + '/goods.json', 'r') as f:
                            data = json.load(f)
                            global goods
                            goods = data
                        return func(goods=data)
                    else:
                        print('>>> 对不起，您的账号或密码错误，请重新输入')
                        count += 1

                else:
                    exit('>>> 对不起，您输入的密码次数过多')

        else:
            return func(goods)

    return inner


@is_superuser
def edit_goods_lst(**kwargs):
    goods = kwargs.get('goods')
    while True:
        code = input('>>> 输入您要修改的产品的编号: ')
        if code.isdigit():
            if code in goods.keys():
                product_info = goods.get(code)
                print('产品名称: %s  价格: %s 元' % (product_info.get('name'), product_info.get('price')))
                choice = input('修改价格？（y）')
                if choice == 'y' or choice == 'yes':
                    new_price = input('>>> 输入新价格: ')
                    if new_price.isdigit():
                        goods[code]['price'] = new_price
                        save_path = DATABASE_MALL.get('path')
                        with open(save_path + '/goods.json', 'w') as f:
                            json.dump(goods, f)
                        print('>>> 修改完成, 产品名称: %s  价格: %s 元'%(goods[code]['name'], goods[code]['price']))

                    else:
                        print('>>> 输入有误')

            else:
                print('>>> 您输入的产品编码不存在')
        else:
            print('>>> 编码必须为数字')

        choice = input('>>> 是否退出？(q)')
        if choice == 'q' or choice == 'quit':
            break
        else:
            pass


@is_superuser
def add_good(**kwargs):
    goods = kwargs.get('goods')
    print(goods)
    print('增加新产品')


def go_shopping():
    """购物功能"""
    shopping_cart = []  # 购物车
    save_path = DATABASE_MALL.get('path')
    # 取出所有商品信息
    with open(save_path+'/goods.json', 'r') as f:
        goods = json.load(f)
    print('欢迎来到ATM购物商城'.center(26, '-'))
    while True:
        print('\n'+'>>> 商品清单如下所示: ')
        print('code'.ljust(6), 'name'.ljust(10), 'price')
        print(''.ljust(26, '-'))
        for k, v in goods.items():
            print(k.ljust(6), goods[k]['name'].ljust(10), goods[k]['price'])
        print(''.ljust(26, '-'))

        choice = input('>>> 请选择要购买的商品(产品编号)/退出购物(q): ')
        if choice == 'q' or choice == 'quit':
            print('>>> 谢谢回顾！')
            break

        else:
            if not choice.isdigit():
                print('>>> 输入有误，请重新输入')
            else:
                if choice not in goods.keys():
                    print('>>> 商品编号输入有误,请重新输入')
                else:
                    price = goods[choice]['price']
                    product_name = goods[choice].get('name', '')
                    tips = input('>>> 将商品%s加进购物车(\033[1;35m (1)\033[0m) 直接购买\033[1;35m (2)'
                                 '\033[0m 清空购物车\033[1;35m (3)\033[0m 请输入编号： ' % product_name)

                    # 将物品加入购物车
                    if tips == '1':
                        shopping_cart.append((product_name, price))

                    # 结账
                    elif tips == '2':
                        shopping_cart.append((product_name, price))
                        payment_amount = 0
                        print('此次购物清单如下'.center(25, '-'))
                        for i in range(len(shopping_cart)):
                            print(shopping_cart[i][0].ljust(10), shopping_cart[i][1])
                            payment_amount += int(shopping_cart[i][1])

                        print('>>> 合计 %s 元' % payment_amount)
                        tips = input('是否立即结账?(y)  ')
                        if tips == 'y' or tips == 'yes':
                            checkout(payment_amount=payment_amount)
                            shopping_cart = []
                        else:
                            print(shopping_cart)

                    # 清空购物车
                    elif tips == '3':
                        shopping_cart = []


