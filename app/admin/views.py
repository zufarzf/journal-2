from flask import abort, Markup, url_for, session, request, current_app, g, redirect
from flask_admin import Admin, AdminIndexView, expose, form
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import validators

import os
from random import random
from uuid import uuid4


from app.admin import admin_panel
# from app.main.views import arr
from app.models import *
from app import app, db


file_path=os.path.abspath(os.path.dirname(__name__))
STORAGE = os.path.join(file_path, 'app/main/main-static/file/')

def name_gen_image(model, file_data):
    hash_name = f'{str(uuid4())}'
    return hash_name

def title_gen_file(model, file_data):
    hash_name = f'{str(uuid4())}'
    return hash_name

def title_gen_image(model, file_data):
    hash_name = f'{str(uuid4())}'
    return hash_name


class DashboardView(AdminIndexView):
    @expose('/')
    def index(self, *func):
        if current_user.get_id():
            self.idp = current_user.get_id()
            us = Personal.query.filter_by(id=self.idp).first()
            if current_user.is_authenticated and us.is_admin:

                return self.render('index.html')
        else:
            raise abort(404)

    def is_visible(self):
        # This view won't appear in the menu structure
        return False

admins = Admin(app, name='Admin', template_mode='bootstrap3', index_view=DashboardView())


class RekvizitView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    column_labels = {
        'id': 'ID',
        'file': 'Файл',
        'text': 'Загаловок',
        'author': 'Авторы',
        'views': 'Abstract views',
        'current': 'Current',
        'just': 'Just accepted',
        'vol_cat': 'Категории',
    }

    form_widget_args = {
        'file':{
            'readonly':True
        },
    }
    # form_columns = ('text', 'author', 'views', 'current', 'just', 'vol_cat')

    # create_modal = True
    # edit_modal = True

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        # url = 'main/main-static/storage/links/' + model.image
        url = url_for('main.static', filename=os.path.join('file/', model.path))

        if model.type in ['doc', 'docx', 'pdf', 'xls', 'pptx']:
            return Markup(f'<a href={url} target="_blank">File</a>')

    form_extra_fields = {
        "file": form.FileUploadField(
            base_path=STORAGE
        )}

    column_formatters = {
        'path': _list_thumbnail
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data
            if storage_file is not None:
                hash = random.getrandbits(128)
                ext = storage_file.filename.split('.')[-1]
                new_filename = f'{hash}.{ext}'
                # create_date = datetime.datetime.now()

                storage_file.save(
                    os.path.join(STORAGE, new_filename)
                )

                _form.name.data = _form.name.data or storage_file.filename
                _form.path.data = new_filename
                _form.type.data = ext

                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        return self._change_path_data(
            super(RekvizitView, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(RekvizitView, self).create_form(obj)
        )



class SmcView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


    column_labels = {
        'id' : 'ID',
        'name' : 'Название',
        'volume' : 'Файлы',
    }

    can_export = True
    create_modal = True
    edit_modal = True

    form_widget_args = {
        'volume': {
            'readonly': True
        },
    }


class EmailView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


    column_labels = {
        'id' : 'ID',
        'title' : 'Загаловок',
        'text' : 'Текст',
        'email' : 'эл-почта',
    }

    can_export = True
    create_modal = True
    edit_modal = True

    form_widget_args = {
        'volume': {
            'readonly': True
        },
    }


class UsersView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


    column_labels = {
        'id' : 'ID',
        'login' : 'Логин',
        'psw' : 'Пароль',
        'is_admin' : 'Админ',
    }

    form_args = {
        'login':dict(validators=[validators.DataRequired()]),
        'psw':dict(validators=[validators.DataRequired()])
    }

    def on_model_change(self, view, model, is_created):
        model.psw = generate_password_hash(model.psw)

    column_hide_backrefs = False
    column_list = ('login', 'psw', 'is_admin')
    can_export = True
    create_modal = True
    edit_modal = True

admins.add_view(SmcView(VolumeCat, db.session, 'Категории'))
admins.add_view(RekvizitView(VolumeInfo, db.session, 'Файл'))
admins.add_view(EmailView(Email, db.session, 'Эл-почта'))
admins.add_view(UsersView(Personal, db.session, 'Админы'))