# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 19:21
# @Author  : Leey
# @Site    :
# @File    : web.py
# @Software: PyCharm


from . import web
from flask import render_template, request, redirect, url_for, flash

from ..forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm, ChangePasswordForm
from ..models.user import User
from app.models.base import db
from flask_login import login_user, logout_user, current_user


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)

        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 将用户票据写入cookie中, 默认保存365天
            login_user(user, remember=True)
            # 如果刚引导未登录用户登录完成,则重定向到登陆之前想要访问的页面
            next = request.args.get('next')
            #                  ↓防止重定向攻击
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash("账号不存在或者密码错误!!")
    return render_template('auth/login.html', form=form)


# 忘记密码
@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    from app.mylib.email import send_mail
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            # 用 first_or_404 当查询失败的时候, 会抛出一个异常, 后续代码也不会执行了.该异常是httpexception的子类.
            # 在web.__init__中用装饰器对404请求进行监听处理,实现返回自己的404页面
            user = User.query.filter_by(email=form.email.data).first_or_404()
            send_mail(form.email.data, '重置你的密码', 'email/reset_password.html', user=user, token=user.generate_token())
            flash('一封邮件已经发送到邮箱' + form.email.data + '请查收!')
    return render_template('auth/forget_password_request.html', form=form)


# 重置密码
@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('重置密码成功', form.password1.data)
            return redirect(url_for('web.login'))
        else:
            flash('重置密码失败!')

    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('auth/change_password.html')
    form = ChangePasswordForm(request.form)
    print(form.old_password.data, form.new_password1.data, form.new_password2.data)
    if not form.validate():
        flash('请规范填写!')
        return redirect(url_for('web.change_password'))

    old_password = form.old_password.data
    if not current_user.check_password(old_password):
        flash('旧密码错误!')
        return redirect(url_for('web.change_password'))

    if form.new_password1.data == form.new_password2.data:
        current_user.change_password(form.new_password1.data)
        flash('重置密码成功!请您牢记!')

    return redirect(url_for('web.login'))


# 注销登录
@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
