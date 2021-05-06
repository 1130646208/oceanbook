#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 21:59
# @Author  : wsx
# @Site    : 
# @File    : yushu_book.py
# @Software: PyCharm
from app.mylib.myhttp import HTTP
from flask import current_app  # 导入当前实例

class YuShuBook:
    # per_page = 15 移动到setting里了
    # 先查找实例变量,再查找类变量
    # 类变量
    isbn_url = 'https://search.douban.com/book/subject_search?search_text={}'
    key_word_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    get_book_id_url = 'https://frodo.douban.com/api/v2/search/weixin?q={}&start=0&count=20&apiKey=0ac44ae016490db2204ce0a042db2916'

    def __init__(self):
        # 实例变量
        self.total = 0
        self.books = []

    def search_by_id(self, book_id):
        # 先查找实例变量,再查找类变量
        item = HTTP().get_by_id(book_id)
        t = {}
        t['book_id'] = ''
        t['title'] = ''
        t['publisher'] = ''
        t['pages'] = ''
        t['price'] = ''
        t['summary'] = ''
        t['image'] = ''
        t['author'] = ''
        t['isbn'] = ''
        t['publisher'] = ''
        t['pubdate'] = ''
        t['binding'] = ''

        t['book_id'] = book_id
        t['title'] = item['title']
        t['image'] = item['img']
        t['summary'] = ''.join(item['content']) or ''
        _info = item['info']
        for info in _info:
            if '作者' in info:
                t['author'] = info.replace('作者:', '')
            elif '出版社' in info:
                t['publisher'] = info.replace('出版社:', '')
            elif '出版年' in info:
                t['pubdate'] = info.replace('出版年:', '')
            elif '页数' in info:
                t['pages'] = info.replace('页数:', '')
            elif '定价' in info:
                t['price'] = info.replace('定价:', '')
            elif '装帧' in info:
                t['binding'] = info.replace('装帧:', '')
            elif 'ISBN' in info:
                t['isbn'] = info.replace('ISBN:', '')

            if t['title']: self.books.append(t)
        self.__fill_single(t)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):

        if data:
            for item in data['books']:
                t = {}
                t['book_id'] = ''
                t['title'] = ''
                t['publisher'] = ''
                t['pages'] = ''
                t['price'] = ''
                t['summary'] = ''
                t['image'] = ''
                t['author'] = ''
                t['isbn'] = ''
                t['publisher'] = ''
                t['pubdate'] = ''
                t['binding'] = ''

                t['book_id'] = item['id']
                t['title'] = item['title']
                t['image'] = item['img']
                t['summary'] = ''.join(item['content']) or ''
                _info = item['info']
                for info in _info:
                    if '作者' in info:
                        t['author'] = info.replace('作者:', '')
                    elif '出版社' in info:
                        t['publisher'] = info.replace('出版社:', '')
                    elif '出版年' in info:
                        t['pubdate'] = info.replace('出版年:', '')
                    elif '页数' in info:
                        t['pages'] = info.replace('页数:', '')
                    elif '定价' in info:
                        t['price'] = info.replace('定价:', '')
                    elif '装帧' in info:
                        t['binding'] = info.replace('装帧:', '')
                    elif 'ISBN' in info:
                        t['isbn'] = info.replace('ISBN:', '')

                if t['title']: self.books.append(t)
            self.total = data['total']


    def search_by_keyword(self, keyword, page=1):
        # url = self.key_word_url.format(keyword, current_app.config['PER_PAGE'], YuShuBook.__cal_start(page))
        url = self.get_book_id_url.format(keyword)
        result = HTTP().get(url)
        self.__fill_collection(result)

    def __cal_start(page):
        return current_app.config['PER_PAGE'] * (page - 1)

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
