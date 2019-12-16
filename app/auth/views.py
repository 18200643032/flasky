from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user
from . import auth
from .. import db
from ..email import send_email   
from ..models import User
from .forms import LoginForm,RegistrationForm,ChangePasswordForm
from ..log import *
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('用户名密码无效')
    return render_template('auth/login.html',form=form)

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已更新')
            return redirect(url_for('main.index'))
        else:
            flash('无效密码')
    return render_template("auth/change_password.html",form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm your account','mail/new_user',user=user,token=token)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

#确认用户的账户
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('已确认你的账户,谢谢')
    else:
        flash('链接无效或过期')
    return redirect(url_for('main.index'))


#过滤未确认的函数
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
       # if not current_user.confirmed and request.endpoint[:5] != 'auth':

        if not current_user.confirmed \
           and request.endpoint \
           and request.blueprint != 'auth' \
           and request.endpoint != 'static':    
#if current_user.is_authenticated() and not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

#重新发送邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm your account','mail/new_user',user=current_user,token=token)
    flash('已经重新发送邮件了')
    return redirect(url_for('main.index'))
