#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/7/5 14:55
# @Author  : wsx
# @File    : wish.py
# @Software: PyCharm
# @Function: ...

from app.models.base import Base,db
from sqlalchemy import Integer, Column, Boolean, String, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.spider.book_ocean import YuShuBook


class Wish(Base):
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

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_id(self.book_id)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False). \
            order_by(desc(Wish.create_time)).all()

        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        # 分组统计
        # query(返回查询出的每个isbn对应的想要的人的数量).filter(没有赠送出去,查询一组isbn,没有删除)
        count_list = db.session.query(func.count(Gift.id), Gift.book_id). \
            filter(Gift.launched == False, Gift.book_id.in_(isbn_list), Gift.status == 1). \
            group_by(Gift.book_id).all()

        count_list = [{'count': gift[0], 'book_id': gift[1]} for gift in count_list]

        # 这样返回使代码更容易阅读
        return count_list
