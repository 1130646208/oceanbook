#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 23:01
# @Author  : wsx
# @Site    : 
# @File    : __init__.py
# @Software: PyCharm
from flask import Flask
from app.web import web
from app.models.base import db
from app.models.user import login_manager
from flask_mail import Mail

mail = Mail()


def create_app():
    # static_folder 存放静态文件的默认目录, 默认是static
    app = Flask(__name__, static_folder='static')
    # 加载配置文件
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    # 注册蓝图
    register_blueprint(app)
    # login_manage
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'  # 指定将未授权用户引导到页面...
    login_manager.login_message = '请先登录或注册'  # 指定对未登录用户闪现消息
    # 注册flask_mail插件
    mail.init_app(app)
    # 在数据库中生成数据表
    db.init_app(app)
    db.create_all(app=app)
    return app


def register_blueprint(app):
    app.register_blueprint(web)
