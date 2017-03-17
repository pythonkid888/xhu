#-*- coding:utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired
from ..models import Category


class AddEventForm(FlaskForm):
    title = StringField('事件', validators= [DataRequired()])
    category = SelectField('类别', coerce= int)
    submit = SubmitField('添加')
    
    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                for category in Category.query.order_by(Category.name).all()]

    
class AddCategoryForm(FlaskForm):
    name = StringField('类别', validators= [DataRequired()])
    submit = SubmitField('添加')
    
    def validate_name(self, field):
        if Category.query.filter_by(name = field.data).first():
            raise ValidationError('类别已存在')
 
        
class EditEventForm(FlaskForm):
    title = StringField('事件', validators= [DataRequired()])
    category = SelectField('类别', coerce= int)
    submit = SubmitField('修改')
    
    def __init__(self, *args, **kwargs):
        super(EditEventForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                for category in Category.query.order_by(Category.name).all()]