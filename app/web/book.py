#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 22:25
# @Author  : wsx
# @Site    : 
# @File    : book.py
# @Software: PyCharm
from flask import request, render_template, flash
from flask_login import current_user
from app.mylib.helper import is_isbn_or_key
from app.spider.book_ocean import YuShuBook
from . import web
from app.forms.book import SearchForms
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from app.models.gift import Gift
from app.models.wish import Wish


# 用蓝图做路由
@web.route("/book/search")
def search():
    """
    q 查询关键字或者isbn
    page
    """
    # 实例化验证器
    form = SearchForms(request.args)
    books = BookCollection()
    if form.validate():
        # 从验证器中取出参数,默认值还在
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)

        elif isbn_or_key == 'key':
            yushu_book.search_by_keyword(q, page=page)

        # return json.dumps(result), 200, {'content-type': 'application/json'}
        books.fill(yushu_book, q)
        # return jsonify(books)
        # 对象不能被序列化成json, 那就把对象的字典序列化成json, 对象中还包含对象的话, 用json.dumps()的default参数指定对对象的操作
        # return json.dumps(books, default=lambda o: o.__dict__)

    else:
        flash('关键字不合要求!')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<id>/detail')
def book_detail(id):
    has_in_gifts = False
    has_in_wishs = False

    # 获取书籍的详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_id(id)
    book = BookViewModel(yushu_book.first)

    # 判断用户是否登录
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, book_id=book.book_id, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, book_id=book.book_id, launched=False).first():
            has_in_wishs = True

    # 获取书籍的赠送清单与心愿清单
    trade_gifts = Gift.query.filter_by(book_id=book.book_id, launched=False).all()
    trade_wishes = Wish.query.filter_by(book_id=book.book_id, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,has_in_wishs = has_in_wishs,has_in_gifts=has_in_gifts)
