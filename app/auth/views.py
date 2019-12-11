from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required
from . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    print('***********')
    if form.validate_on_submit():
        print('......................')
        user = User.query.filter_by(email=form.email.data).first()
        print('----------')
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            print(123)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名密码无效')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))