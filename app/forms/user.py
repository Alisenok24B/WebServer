from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):  # register form
    name = StringField('Имя пользователя', validators=[DataRequired()])  # name
    password = PasswordField('Пароль', validators=[DataRequired()])  # password
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])  # password again
    date = DateField('Дата рождения', format='%d.%m.%Y', validators=[DataRequired()])  # date of birth
    submit = SubmitField('Зарегистрироваться')  # button register


class LoginForm(FlaskForm):  # login form
    name = StringField('Имя пользователя', validators=[DataRequired()])  # name
    password = PasswordField('Пароль', validators=[DataRequired()])  # password
    remember_me = BooleanField('Запомнить меня')  # check box remember me
    submit = SubmitField('Войти')  # button go
