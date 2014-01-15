#!/usr/bin/env python
#coding=utf-8
#/var/www/weixin/hanzi.py
#nightwish

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


hello   = '''您已关注蟹爪小精灵，请输入注册邮箱和密码，用半角冒号隔开。如注册邮箱为‘123@qq.com’，密码是‘123456’，请回复123@qq.com:123456。'''
help    = '''喵'''

weixin  = '''微信'''

bind_ok = '''绑定成功'''
send_ok = '''发送成功'''

sendfrom_ok   = '''尾巴成功更改为''' + ':'
sendfrom_fail = '''尾巴更改失败'''
