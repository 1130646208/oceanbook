#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/6/2 16:46
# @Author  : wsx
# @File    : book.py
# @Software: PyCharm
# @Function: 书籍的模型
from app.models.base import Base
from sqlalchemy import String, Integer, Column


class Book(Base):
    """书籍信息"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未命名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    book_id = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
