#-*- coding:utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from ..models import User

class LoginForm(FlaskForm):

    email = StringField('邮箱', validators = [DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators = [DataRequired()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):

    email = StringField('邮箱', validators= [DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators= [DataRequired(), Length(1, 64),
                                                    Regexp('^[a-zA-Z][a-zA-Z0-9._]*$', 0,
                                                           'consist of letters,numbers, dots or underscores')])
    password = PasswordField('密码', validators= [DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(),
                                                              EqualTo('password', message= 'password must match')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email= field.data).first():
            raise ValidationError('邮箱已注册')

    def validate_username(self, field):
        if User.query.filter_by(username= field.data).first():
            raise ValidationError('用户名已占用')

class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('新密码', validators= [DataRequired()])
    password2 = PasswordField('确认密码', validators= [DataRequired(), EqualTo('new_password',
                                                                                  message = 'password must match')])
    submit = SubmitField('确认')

class ResetRequestForm(FlaskForm):
    email = StringField('注册邮箱', validators= [DataRequired()])
    submit = SubmitField('提交')

class ResetPasswordForm(FlaskForm):
    email = StringField('邮箱', validators= [DataRequired()])
    new_password = PasswordField('新密码', validators= [DataRequired()])
    password2 = PasswordField('确认密码', validators= [DataRequired(), EqualTo('new_password',
                                                                                  message= 'password must match')])
    submit = SubmitField('重置')
