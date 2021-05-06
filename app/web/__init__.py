#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 23:01
# @Author  : wsx
# @Site    : 
# @File    : __init__.py
# @Software: PyCharm


# 蓝图
from flask import Blueprint, render_template
# 如果蓝图有自己的静态文件, 也可以指定静态文件夹
web = Blueprint('web', __name__, static_folder='', static_url_path='')


# 监控所有404异常, 返回自己想要的页面
@web.app_errorhandler(404)
def not_found(e):
    # AOP思想,面向切片思想
    return render_template('404.html'), 404


# 导入即运行
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
