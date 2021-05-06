# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 19:21
# @Author  : Leey
# @Site    : 
# @File    : web.py
# @Software: PyCharm


from flask import request, flash, render_template
from flask_login import current_user, UserMixin

from app.forms.book import SearchForm
from app.lib.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.book_ocean import YuShuBook
from app.view_models.book import BookCollection, BookViewModels
from app.view_models.trade import TradeInfo
from . import web

'''
    1、判断获取数据对类型，如果是isbn编号则使用YuShuBook.search_by_isbn（q）查询，
        否则使用关键字查询YuShuBook.search_by_keyword(q, page=page)
    2、序列化需要返回对数据
'''


@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()  # 从验证通过的form中取值，保证数据对正确性
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)  # 这里将对象进行json序列化。
    else:
        # return jsonify(form.errors)
        flash("搜索的关键字不符合要求，请重新输入关键字")
    return render_template('search_result.html', books=books)


# 书籍详情页面
@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishs = False

    # 获取书籍的详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModels(yushu_book.first)

    # 判断用户是否登录
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishs = True

    # 获取书籍的赠送清单与心愿清单
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,has_in_wishs = has_in_wishs,has_in_gifts=has_in_gifts)

filter