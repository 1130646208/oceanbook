# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 19:21
# @Author  : wsx
# @Site    :
# @File    : web.py
# @Software: PyCharm


from . import web

from flask import render_template, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.base import db
from app.models.wish import Wish
from app.models.gift import Gift


# 心愿清单
@web.route('/my/wish')
def my_wish():
    from app.view_models.wish import MyWishes
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    book_id_list = [wish.book_id for wish in wishes_of_mine]
    wish_count_list = Wish.get_gift_counts(book_id_list)
    view_model = MyWishes(wishes_of_mine, wish_count_list)
    return render_template('my_wish.html', wishes=view_model.wishes)


@web.route('/gifts/book/<id>/detail')
@login_required
def save_to_wish(id):
    if current_user.can_save_to_list(id):
        with db.auto_commit():
            wish = Wish()
            wish.book_id = id
            # current_user 实际上就是实例化的User(), 在models.user中的get_user()中将uid转化成User()实例模型
            wish.uid = current_user.id
            db.session.add(wish)
            flash('添加成功!')

    else:
        flash('这本书已经存在于赠送清单或者心愿清单, 请不要重复添加.')
    return redirect(url_for('web.book_detail', id=id))


# 向其他人赠送此书
# 1、想他人发送邮件
# 2、他人通过邮件来接送此书
@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    from app.mylib.email import send_mail
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(
        uid=current_user.id,
        book_id=wish.book_id).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。'
              '添加前，请确保自己可以赠送此书')
    else:
        send_mail(wish.user.email, '有人想送你一本书',
                  'email/satisify_wish.html', gift=gift,wish=wish)
        flash('已向他/她发送一封邮件，如果他/她愿意接受你对赠送，'
              '你将收到一个漂流瓶')
    return redirect(url_for('web.book_detail', id=wish.book_id))



# 撤销心愿
@web.route('/wish/book/<id>/redraw')
@login_required
def redraw_from_wish(id):
    wish = Wish.query.filter_by(
        book_id=id,
        launched=False,
    ).first_or_404()
    with db.auto_commit():
        db.session.delete(wish)
    return redirect(url_for('web.my_wish'))

