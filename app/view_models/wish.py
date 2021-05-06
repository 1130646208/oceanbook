#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/7/17 21:51
# @Author  : wsx
# @File    : wish.py
# @Software: PyCharm
# @Function: ...
from app.view_models.book import BookViewModel


class MyWishes:
    def __init__(self, wishes_of_mine, wish_count_list):
        self.wishes = []

        self.__wishes_of_mine = wishes_of_mine
        self.__wish_count_list = wish_count_list

        self.wishes = self.__parse()

    def __parse(self):
        temp_wishes = []
        for wish in self.__wishes_of_mine:
            my_wish = self.__matching(wish)
            temp_wishes.append(my_wish)

        return temp_wishes

    def __matching(self, wish):
        count = 0
        for wish_count in self.__wish_count_list:
            if wish_count['book_id'] == wish.book_id:
                count = wish_count['count']

        r = {
            'wishes_count': count,
            'book': BookViewModel(wish.book),
            'id': wish.id
        }
        return r
