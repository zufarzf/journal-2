from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from flask_ckeditor import CKEditorField


class AddForm(FlaskForm):
    author = CKEditorField('Автор')
    abstract = CKEditorField('Abstract')
    cite = CKEditorField('Cite')
    submit = SubmitField("Отправить")


class Fancy(FlaskForm):
    radio = RadioField(choices=[('yes','Да'),('no','Нет')])