#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/7/12 14:36
# @Author  : wsx
# @File    : trade.py
# @Software: PyCharm
# @Function: ...


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


class MyTrades:
    """将wish和gift抽象成trade"""
    pass
