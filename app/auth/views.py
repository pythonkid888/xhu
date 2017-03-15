

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ResetRequestForm, ResetPasswordForm
from ..models import User
from .. import db
from ..emails import send_email


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid email or password')
    return render_template('auth/login.html', form = form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        flash('User has registered Successfully')
        token = user.generate_confirmation_token()
        send_email(user.email, 'confirm email', 'auth/mail/confirm', user = user, token = token)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account')
    else:
        flash('Your token invalid or timed out')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            flash('You have not confirmed your account yet')
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'a confirmation mail', '/auth/mail/confirm', token = token)
    flash('a new confirmation email has been sent to you')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        db.session.add(current_user)
        flash('change password successfully')
        return redirect(url_for('auth.login'))
    return render_template('auth/accountset.html', form = form)


@auth.route('/reset-request', methods= ['GET', 'POST'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            flash('email error')
        token = user.generate_reset_token()
        send_email(user.email, 'find password', 'auth/mail/find_password', token = token)
        flash('an email has been sent to you')
        return redirect(url_for('main.index'))
    return render_template('auth/accountset.html', form = form)


@auth.route('/reset_password/<token>', methods= ['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if not current_user.is_anonymous:
            return redirect(url_for('main.index'))
        user = User.query.filter_by(email = form.email.data).first()
        if not user:
            flash('email error')
        if not user.verify_token(token):
            flash('token invalid or timed out')
        else:
            user.password = form.new_password.data
            db.session.add(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/accountset.html', form = form)


