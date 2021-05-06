#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/7/25 20:42
# @Author  : wsx
# @File    : enums.py
# @Software: PyCharm
# @Function: 枚举类型
from enum import Enum


class PendingStatus(Enum):
    """交易状态"""
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4

    @classmethod
    def pending_str(cls, pending, you_are):
        res = ''
        if pending == cls.Waiting.value:
            if you_are == 'gifter':
                res = '等待对方确认接收.'
            else:
                res = '等待对方同意赠送.'
        elif pending == cls.Success.value:
            if you_are == 'gifter':
                res = '书籍赠送成功!'
            else:
                res = '书籍索要成功!'
        elif pending == cls.Reject.value:
            if you_are == 'gifter':
                res = '您已拒绝.'
            else:
                res = '对方已拒绝.'
        elif pending == cls.Redraw.value:
            if you_are == 'gifter':
                res = '您已撤销.'
            else:
                res = '对方已撤销.'
        return res
