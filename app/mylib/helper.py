#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 21:25
# @Author  : wsx
# @Site    : 
# @File    : helper.py
# @Software: PyCharm


def is_isbn_or_key(q) -> str:
    """
    isbn13，13位数字组成
    isbn10,10位数字组成，可能包括 -
    """
    isbn_or_key = 'key'
    short_q = q.replace('-', '')
    if len(short_q) == 13 and short_q.isdigit():
        isbn_or_key = 'isbn'
    elif len(short_q) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
