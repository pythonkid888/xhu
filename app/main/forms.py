#-*- coding:utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import User, Role
from flask_pagedown.fields import PageDownField

class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators= [Length(0, 64)])
    location = StringField('所在地', validators= [Length(0, 64)])
    about_me = TextAreaField('简介')
    submit = SubmitField('提交')

class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators= [DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators= [DataRequired(), Length(1, 64),
                                                    Regexp('^[a-zA-Z][a-zA-Z0-9._]*$', 0,
                                                    'Username must consis of letters, numbers, dots, undersorces')])
    confirmed = BooleanField('激活状态')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators= [Length(0, 64)])
    location = StringField('所在地', validators= [Length(0, 64)])
    about_me = TextAreaField('简介')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email = field.data).first():
            raise ValidationError('邮箱已注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已存在')

class PostForm(FlaskForm):
    body = PageDownField("状态", validators= [DataRequired()])
    submit = SubmitField('提交')

class CommentForm(FlaskForm):
    body = PageDownField('评论', validators= [DataRequired()])
    submit = SubmitField('提交')


