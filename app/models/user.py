#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/6/6 21:44
# @Author  : wsx
# @File    : user.py
# @Software: PyCharm
# @Function: ...
from math import floor

from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import Base, db
from sqlalchemy import String, Integer, Column, Boolean, Float
from flask_login import UserMixin
from flask_login import LoginManager
from flask import current_app

from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.mylib.helper import is_isbn_or_key
from app.mylib.enums import PendingStatus
from app.spider.book_ocean import YuShuBook

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

login_manager = LoginManager()


# 以下三行不加会报错
@login_manager.user_loader
def load_user(user_id):
    return None


# UserMixin是管理cookie的
class User(UserMixin, Base):
    # __tablename__ = '自定义表名'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    # 预留的小程序接口
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    # 对密码进行加密处理
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        # 将raw加密之后和_password对比
        return check_password_hash(self._password, raw)

    # # 下面函数是 flask_login 要求的函数名, 不想直接定义就继承UserMixin(如上所示).
    # 另外需要注意的是, 如果我们的项目中用户id不是用id字段表示的,那么需要override get_id()函数.并返回项目中实际的用户id字段
    # def get_id(self):
    #     return self.id

    def can_save_to_list(self, book_id):
        # 系统能查到才能赠送
        # if is_isbn_or_key(book_id) != 'isbn':
        #     return False
        yushubook = YuShuBook()
        yushubook.search_by_id(book_id)
        book = yushubook.first

        if not book:
            return False
        # 不允许一个用户赠送多本相同图书
        # 一个用户不能同时成为请求者和索要着

        # 既不在心愿清单也不在赠送清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, book_id=book_id,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, book_id=book_id,
                                       launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # 当token过期时, serializer会抛出异常
            data = s.loads(token.encode('utf-8'))
            uid = data.get('id')
        except Exception:

            return False
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password

        return True

    def change_password(self, new_password):
        try:
            with db.auto_commit():
                self.password = new_password
        except Exception:
            return False

        return True

    # 判断是否在自己的礼物中或者心愿中
    def has_in_trades(self, book_id, trade_type):
        if trade_type == 'wish':
            if Wish.query.filter_by(book_id=book_id, uid=self.id).first():
                return True
            else:
                return False

        if trade_type == 'gift':
            if Gift.query.filter_by(book_id=book_id, uid=self.id).first():
                return True
            else:
                return False

    def can_send_drift(self):
        # 检测是否能够发起交易:
        # 2 鱼豆数量必须足够
        # 3 每索取两本书, 必须送出一本书

        # 鱼豆不足
        if self.beans < 1:
            return False
        # 成功收到礼物数量
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        # 成功送出礼物数量
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        # 每索取两本书必须送出一本书
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False
        # return True if success_receive_count / success_gifts_count <= 2 else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


# 为加入登陆权限,为login_required插件编写的函数
# 导入app文件夹下的init文件中的login_manager
# 加装饰器才能让flask_login_in调用
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))  # 不需要用filter_by因为查询的是主键
