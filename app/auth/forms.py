from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User


#登录的表单
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(1,64)])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Keep me log')
    submit = SubmitField('登录')



#注册的表单
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    username = StringField('Username',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only lettersaada')])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField('注册')


    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')
   
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('有户名已存在')

#更改密码的表单
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧的密码',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField('确认更改')

