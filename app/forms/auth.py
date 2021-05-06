#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/6/7 20:52
# @Author  : wsx
# @File    : auth.py
# @Software: PyCharm
# @Function: ...

from wtforms import Form, StringField, PasswordField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[Length(8, 64), DataRequired(), Email(message='数据不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少2个字符,最多10个字符.')])

    # validate_email命名是固定的,这样wtforms会自动将客户端的email数据传入到field中
    def validate_email(self, field):
        # 查询数据库中是否已经存在相同的邮箱
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已经存在!')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已经存在!')


class LoginForm(Form):
    email = StringField(validators=[Length(8, 64), DataRequired(), Email(message='数据不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮件不符合规范!')])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='密码长度应该是6-32字符.'),
        EqualTo('password2', message='两次输入不一致!')
    ])
    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32),
    ])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])
    new_password1 = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='密码长度应该是6-32字符.'),
        EqualTo('new_password2', message='两次输入不一致!')
    ])
    new_password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32),
    ])
