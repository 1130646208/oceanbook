# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 0:24
# @Author  : wsx
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from flask import render_template
from flask_login import login_required, current_user
from . import web
from app.models.gift import Gift


# 默认展示最新上传的30条礼物清单列表
from ..view_models.book import BookViewModel


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@login_required
@web.route('/personal')
def personal_center():
    user = current_user
    return render_template('personal.html', user=user)

