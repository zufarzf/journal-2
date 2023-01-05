from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email

class LoginForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min = 4, message="Loginni kiriting!")], render_kw={'placeholder' : 'Login...'})
    psw = PasswordField(validators=[DataRequired(), Length(min=4, max = 50, message="Parolni to'g'ri kiriting!")], render_kw={'placeholder' : 'Parol...'})
