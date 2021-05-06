# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 19:21
# @Author  : Leey
# @Site    :
# @File    : web.py
# @Software: PyCharm

from flask import current_app, flash, redirect, url_for, render_template

from . import web
from flask_login import login_required, current_user
from app.models.base import db
from app.models.gift import Gift
from ..models.drift import Drift
from ..mylib.enums import PendingStatus
from ..view_models.gift import MyGifts


# 赠送清单
@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    book_id_list = [gift.book_id for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(book_id_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.gifts)
    # return 'gifts'


@web.route('/gifts/book/<id>')
@login_required
def save_to_gifts(id):
    if current_user.can_save_to_list(id):
        with db.auto_commit():
            gift = Gift()
            gift.book_id = id
            # current_user 实际上就是实例化的User(), 在models.user中的get_user()中将uid转化成User()实例模型
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
        flash('此书已经成功添加到你到赠送清单')
    else:
        flash('这本书已经存在于赠送清单或者心愿清单, 请不要重复添加.')

    return redirect(url_for('web.book_detail', id=id))


# 撤销赠送书籍
@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    # 判断这个礼物是否处于交易状态，
    # 处于交易状态是不能直接撤销的
    drift =Drift.query.filter_by(
        gift_id=gid,
        pending=PendingStatus.Waiting
    ).first()
    if drift:
        flash('这个礼物正处于交易状态，请前往【漂流瓶】完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.delete(gift)
    return redirect(url_for('web.my_gifts'))
