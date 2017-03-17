#-*- coding:utf-8 -*-


from . import todo
from flask_login import login_required, current_user
from ..models import Event, Category
from .forms import AddEventForm, AddCategoryForm, EditEventForm
from .. import db
from flask import redirect, url_for, flash, render_template


@todo.route('/show')
def show():
    events = Event.query.filter_by(sponsor_id = current_user.id).all()
    if events is None:
        flash('你还未创建任何事项')
    return render_template('todo/show.html', events = events)


@todo.route('/add-event', methods = ['GET', 'POST'])
@login_required
def add_event():
    form = AddEventForm()
    if form.validate_on_submit():
        event = Event(title = form.title.data,
                      category = Category.query.get(form.category.data).name,
                      sponsor = current_user._get_current_object()
                     )
        db.session.add(event)
        flash('添加事件成功')
        return redirect(url_for('todo.show'))
    return render_template('todo/add_event.html', form = form)


@todo.route('/add-category', methods = ['GET', 'POST'])
@login_required
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category(name = form.name.data)
        db.session.add(category)
        flash('添加类别成功')
        return redirect(url_for('todo.show'))
    return render_template('todo/add_category.html', form = form)


@todo.route('/edit-event/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EditEventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.category = Category.query.get(form.category.data).name
        db.session.add(event)
        flash('事件已更新')
        return redirect(url_for('.show'))
    form.title.data = event.title
    form.category.data = event.category
    return render_template('todo/edit_event.html', form = form)


@todo.route('/delete-event/<int:id>', methods= ['GET', 'POST'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('.show'))


@todo.route('/finish/<int:id>')
@login_required
def finish(id):
    event = Event.query.get_or_404(id)
    if event:
        event.completion = True
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('.show'))