#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/7/25 20:21
# @Author  : wsx
# @File    : drift.py
# @Software: PyCharm
# @Function: 鱼漂模型
from app.models.base import Base
from sqlalchemy import Column, Integer, String, SmallInteger


class Drift(Base):
    """
    一次交易的具体信息
    """
    pending = Column(SmallInteger, default=0, nullable=False)

    # 邮寄信息
    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    book_id = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_image = Column(String(200))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
