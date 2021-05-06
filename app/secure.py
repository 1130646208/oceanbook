#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 20:59
# @Author  : wsx
# @Site    : 
# @File    : secure.py.py
# @Software: PyCharm

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:1234@localhost:3306/fisher'

SECRET_KEY = 'qwertyahgfbcngjskhogksjghsnebgiu'

# email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '1130646208@qq.com'
# 授权码
MAIL_PASSWORD = 'qbmffrgrjtmqgdhh'

# 这两个好像没用
# MAIL_SUBJECT_PREFIX = '[鱼书]'
# MAIL_SENDER = '鱼书 <hello@yshu.im>'
