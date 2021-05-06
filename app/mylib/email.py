#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/7/24 23:14
# @Author  : wsx
# @File    : email.py
# @Software: PyCharm
# @Function: 发送电子邮件给用户重置密码

from app import mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread


def send_mail(to, subject, template, **kwargs):
    # 标题, 发送者(不能写错,写自己的),
    # msg = Message('测试邮件', sender='1130646208@qq.com', body='Test!!!', recipients=['1130646208@qq.com'])
    # mail.send(msg)
    msg = Message('[王双星的书海] ' + subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 拿到真实的核心对象
    app = current_app._get_current_object()
    t = Thread(target=send_async_email, args=[msg, app])
    t.start()


def send_async_email(msg, app):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
