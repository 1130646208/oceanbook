#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/29 16:42
# @Author  : wsx
# @Site    : 
# @File    : user.py
# @Software: PyCharm
from . import web


@web.route('/login')
def login():
    return 'login~'
    pass
