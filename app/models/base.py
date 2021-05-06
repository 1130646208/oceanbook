#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/6/6 21:45
# @Author  : wsx
# @File    : base.py
# @Software: PyCharm
# @Function: 基础模型
from datetime import datetime

from sqlalchemy import Column, Integer, SmallInteger
from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager


class SubSQLAlchemy(SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            raise e


db = SubSQLAlchemy()


class Base(db.Model):
    """定义一个基类,抽象出一些模型共有的属性"""
    # 不希望创建这样一张表,只是为了继承
    __abstract__ = True
    create_time = Column('create_time', Integer)
    # 状态,表示数据是否被删除(软删除)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs: dict):
        for key, value in attrs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def create_datetime(self) -> str:
        if self.create_time:
            return datetime.fromtimestamp(self.create_time).strftime('%Y-%m-%d')

