#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/6/1 10:28
# @Author  : wsx
# @File    : book.py
# @Software: PyCharm
# @Function: 验证book视图函数参数合法性

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForms(Form):
    # datarequired 传入空格也算错误
    q = StringField(validators=[DataRequired(), Length(min=1, max=30, message='自定义错误提示，q参数出错。')])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class DriftForm(Form):
    recipient_name = StringField(validators=[DataRequired(), Length(min=2, max=20, message='收件人长度必须在2-20字符之间')])
    mobile = StringField(validators=[DataRequired(), Regexp('^1[0-9]{10}$', 0, '请输入正确手机号!')])
    message = StringField()
    address = StringField(validators=[DataRequired(), Length(min=10, max=70, message='地址在10-70字符之间!')])