from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):  # register form
    name = StringField('Имя пользователя', validators=[DataRequired()])  # name
    password = PasswordField('Пароль', validators=[DataRequired()])  # password
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])  # password again
    date = DateField('Дата рождения', format='%d.%m.%Y')  # date of birth
    submit = SubmitField('Зарегистрироваться')  # button register


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
