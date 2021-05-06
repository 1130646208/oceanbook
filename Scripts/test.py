#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 22:34
# @Author  : wsx
# @File    : test.py
# @Software: PyCharm
# @Function: ...

import json


class A:
    def __init__(self):
        self.a = 0
        self.b = 1

    def foo(self):
        print('this is foo')


class B:
    def __init__(self):
        self.c = A()


def main():
    b = B()
    print(json.dumps(b, default=lambda o: o.__dict__))


if __name__ == '__main__':
    main()