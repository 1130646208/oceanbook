#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 21:37
# @Author  : wsx
# @Site    : 
# @File    : myhttp.py
# @Software: PyCharm
import requests
import json
import threading


class HTTP:

    def get(self, url):
        headers = {
            'Host': 'frodo.douban.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,deflate,br',
            'Referer': 'https://servicewechat.com/wx2f9b06c1de1ccfca/82/page-frame.html'

        }
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            pass
            return {}
        else:
            j = json.loads(r.text)
            books_id = []
            if j and j.get('items'):
                items = j['items']
                for item in items:
                    if item['type_name'] == '图书':
                        books_id.append(item['target']['uri'].split('/')[-1])
            books = []
            thread_list = []
            for id in books_id:
                t = threading.Thread(target=self.get_book, args=(id, books))
                thread_list.append(t)
            for th in thread_list:
                th.start()
            for th in thread_list:
                th.join()
            return {'books': books, 'total': len(books)}

    def get_book(self, book_id, res_list):
        r = requests.get('http://39.105.38.10:8081/book/info?id={}'.format(book_id)).text
        j = json.loads(r)
        j['data']['id'] = book_id
        res_list.append(j['data'])

    def get_by_id(self, book_id):
        r = requests.get('http://39.105.38.10:8081/book/info?id={}'.format(book_id)).text
        j = json.loads(r)
        j['data']['id'] = book_id
        return j['data']
