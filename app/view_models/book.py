#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/6/3 23:54
# @Author  : wsx
# @File    : book.py
# @Software: PyCharm
# @Function: view_model, 调整数据便于显示到网页


class BookViewModel:
    """单本数据"""
    def __init__(self, book):
        self.book_id = book['book_id']
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.price = book['price']
        self.summary = book['summary'] or '暂无简介'
        self.image = book['image']
        self.author = book['author']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                       [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    """一组图书的数据"""
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.keyword = keyword
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:
    """废弃不用"""
    @classmethod
    def package_single(cls, data, keyword):
        """用isbn查询，会返回单个结果"""
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword,
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]

        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        """用书籍名称查询，会返回很多结果"""
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword,
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]

        return returned

    @classmethod
    def __cut_book_data(cls, data):
        """裁剪数据,便于显示
        or表达式处理空数据
        """
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image'],
            'author': ', '.join(data['author'])
        }

        return book
