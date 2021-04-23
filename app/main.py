from flask import Flask, render_template
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from werkzeug.utils import redirect
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
from random import choice
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():  # main website
    if current_user.is_authenticated:  # is authenticate user or not
        return redirect('/horoscope')  # see the horoscope
    else:
        with open('static/json/about_horoscope.json', 'r',
                  encoding='utf-8') as joke_file:  # open json file
            data = json.load(joke_file)  # create json object
            index_joke = choice(list(data.keys()))  # choice random joke
    return render_template("index.html",
                           joke=data[index_joke])  # see the main website


@app.route('/register', methods=['GET', 'POST'])
def reqister():  # register
    form = RegisterForm()  # register form
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:  # check password
            return render_template('register.html',  # error
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(
                User.name == form.name.data
        ).first():  # check user in base users
            return render_template('register.html',  # error
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data)  # add user parameters
        user.date_to_sign(form.date.data)  # date to sign and add sign
        user.set_password(form.password.data)  # add user's password
        db_sess.add(user)  # add user
        db_sess.commit()
        return redirect('/login')  # go to the next website
    return render_template('register.html', title='Регистрация',
                           form=form)  # see the register website


@login_manager.user_loader
def load_user(user_id):  # get user for normal flask-login's work
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():  # login
    form = LoginForm()  # login form
    if form.validate_on_submit():
        db_sess = db_session.create_session()  # create session
        user = db_sess.query(User).filter(
            User.name == form.name.data).first()  # find user
        if user and user.check_password(form.password.data):  # check user
            login_user(user, remember=form.remember_me.data)  # remember user
            return redirect("/horoscope")
        return render_template('login.html',  # error
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация',
                           form=form)  # see the login website


@app.route('/logout')
@login_required
def logout():  # forget user and go to main website
    logout_user()
    return redirect("/")


@app.route('/horoscope')
@login_required
def horoscope():  # show horoscope
    with open('static/json/signs.json', 'r',
              encoding='utf-8') as sign_file:  # open json file
        data = json.load(sign_file)
        about_sign = data[current_user.sign]  # information about sign
    with open('static/json/info.json', 'r',
              encoding='utf-8') as info_file:  # open json file
        data = json.load(info_file)
        prediction = data[current_user.sign]  # prediction at the day
    return render_template('horoscope.html',  # see horoscope
                           name=current_user.name,
                           sign=current_user.sign,
                           about_sign=about_sign,
                           prediction=prediction)


def main():
    db_session.global_init("db/horoscope.db")  # connection with database
    app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
