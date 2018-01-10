

# 模拟ATM+购物商城程序

---
## 主要功能如下:
>1. 办理信用卡 :登录状态下无法办理新卡
>2. 账户余额信息查询

>3. 转账
>
>4. 提现
>
>5. 还款 | 充值 : 在最迟还款日之前还款,若余额不足还款,则提示充值
>
>6. 挂失 :直接锁定登录的账户,并且退出当前账号
>
>7. 购物 : 具有购物车的增加物品,清空和结算等功能,结算会直接链接信用卡功能,进行支付
>
>8. 打印账户消费记录 : 选择相应的年和月份,屏幕就会输出当月的所有交易记录
>
>9. 退出: 分两步,先退出当前账号,再退出ATM

---

## 代码结构分布图
![项目目录](http://oyhijg3iv.bkt.clouddn.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE_%E9%80%89%E6%8B%A9%E5%8C%BA%E5%9F%9F_20180110105956.png)

##项目包详细说明
1. management.py
 * 文件为程序主入口, 包含了程序的所有功能,可以直接调用 core包内和shopping_api的所有函数;
2. core/auth.py
 * 用户登录函数 login(): 作为装饰器函数,被accounts_operations.py 内部的功能函数所调用, 具体功能: 1.识别账号的状态信息(锁定,过期); 2. 维持登录状态(避免重复登录)

 * 登出函数 logout(): 仅退出当前账号的登录,随后返回主界面,进行后续操作需要重新登录

 * check_login(): 主要用于 create_new_accounts(),用来检测用户的登录状态,项目设定在登录账号的状态下无法创建新的信用卡,需退出当前用户

3. core/atm.py
 * create_new_accounts(): 办理新卡,若已登录账号,需退出账号,其中账号,密码和还款日期都有相对的规则: 卡号不能重复,且和密码长度必须大于6位, 还款日期必须在每月16-30号之间

 * pay_back_urgently(): 当用户在登录过程中系统检测到当前日期超过了该卡的最迟还款期限,则调用此函数进行还款

4. core/accounts_operations.py.py
 * 包含了以下几项功能: 1,查询用户信息(view_account_info), 2,提现(with_draw), 3,还款|充值(pay_back), 4,转账(transfer), 5,购物结账(checkout), 6,挂失账号(disable_credit_card), 7,查询卡号流水(output_transaction_records)

5. core/logger.py.py
 * 日志文件设置,主要分为access记录和transaction记录,在用户操作完成后调用log_generate函数即可将信息输入到对应的日志

6. shopping_mall/shopping_api.py
 * go_shopping(): 购物界面交互,选择商品编号后加入购物车,若选择结账则调用checkout登录信用卡进行结账
 * 后期扩展功能: 编辑修改商品价格(edit_goods_lst), 以及增加物品(add_good),只有超级用户验证通过才可以进行操作



---
## 具体演示代码:

```
#查询消费记录
>>> 请输入您的信用卡卡号: 333333
>>> 请输入您的密码: abc

-----------登录成功----------
-----开始查询月度消费记录-----
>>> 请输入年: 2018
>>> 请输入月份：　1
2018-01-09 21:21:33,133 INFO 333333 consume ￥9566.0
2018-01-09 21:22:14,107 INFO 333333 transfer ￥-3000 to_111111
2018-01-09 21:22:23,905 INFO 333333 charge ￥20000
2018-01-09 21:22:23,906 INFO 333333 pay_back ￥-12566.0
2018-01-09 21:22:33,022 INFO 333333 withdraw ￥-5000 from_balance
2018-01-09 21:22:53,582 INFO 333333 charge ￥10000
2018-01-09 21:50:02,809 INFO 333333 receive ￥3000 from_555555
2018-01-09 21:50:12,911 INFO 333333 receive ￥200 from_555555

```
---
```
# 购物商城
code   name       price
--------------------------
4      iphone     8888
1      mac_pro    9500
7      jacket     500
6      shoe       422
5      bottle     50
2      mouse      66
3      book       70
--------------------------
>>> 请选择要购买的商品(产品编号)/退出购物(q): 4
>>> 将商品iphone加进购物车(1) 直接购买(2) 清空购物车(3) 请输入编号： 2
---------此次购物清单如下--------
mac_pro    9500
mac_pro    9500
mouse      66
book       70
iphone     8888
>>> 合计 28024 元
是否立即结账?(y)

```

---
## 项目扩展功能







