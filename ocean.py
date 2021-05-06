#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/16 22:36
# @Author  : wsx
# @Site    : 
# @File    : fisher.py
# @Software: PyCharm

from app import create_app

myapp = create_app()
if __name__ == "__main__":
    myapp.run(debug=myapp.config['DEBUG'], port=8000, host='127.0.0.1')
