
# -- coding: utf-8 --
# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 17:11
# @Author  : wsx
# @Site    :
# @File    : drift.py
# @Software: PyCharm
from app.mylib.enums import PendingStatus


# 集合类型

class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = []
        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


# 单体Drift
class DriftViewModel:
    def __init__(self, dirft, current_user_id):
        self.data = {}
        self.data = self.__parse(dirft, current_user_id)

    # 判断是索要者还是赠送者
    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_str = PendingStatus.pending_str(drift.pending, you_are)

        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_image': drift.book_image,
            'date': drift.create_datetime,
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'message': drift.message,
            'address': drift.address,
            'status_str': pending_str,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending
        }
        return r
