#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/6 21:44
# @Author  : wsx
# @File    : gift.py
# @Software: PyCharm
# @Function: ...
from flask import current_app

from app.models.base import Base, db
from app.models.wish import Wish
from sqlalchemy import Integer, Column, Boolean, String, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.spider.book_ocean import YuShuBook


class Gift(Base):
    # 礼物编号
    id = Column(Integer, primary_key=True)
    # 施赠的用户是谁
    # 注意关联方式,是数据库内部关联,不是python中关联,所以加引号
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # 是否已经赠送
    launched = Column(Boolean, default=False)
    # 赠送的书籍isbn
    book_id = Column(String(15), nullable=False)

    @classmethod
    def recent(cls):
        # 链式调用,最后的all()触发查询操作
        recent_gift = Gift.query.filter_by(launched=False).\
            group_by(Gift.book_id).\
            order_by(desc(Gift.create_time)).\
            limit(current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_id(self.book_id)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).\
            order_by(desc(Gift.create_time)).all()

        return gifts

    @classmethod
    def get_wish_counts(cls, book_id_list):
        # 分组统计
        # query(返回查询出的每个isbn对应的想要的人的数量).filter(没有赠送出去,查询一组isbn,没有删除)
        count_list = db.session.query(func.count(Wish.id), Wish.book_id).\
            filter(Wish.launched==False, Wish.book_id.in_(book_id_list), Wish.status==1).\
            group_by(Wish.book_id).all()

        count_list = [{'count': wish[0], 'book_id': wish[1]} for wish in count_list]

        # 这样返回使代码更容易阅读
        return count_list

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False
