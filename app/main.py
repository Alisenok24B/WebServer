from os import abort
from flask import Flask, render_template, request
from data import db_session
from data.users import User
# from data.news import News
from forms.user import RegisterForm, LoginForm
# from forms.news import NewsForm
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from random import choice
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():  # main website
    with open('static/json/anekdot.json', 'r', encoding='utf-8') as joke_file:  # open json file
        data = json.load(joke_file)  # create json object
        index_joke = choice(list(data.keys()))  # choice random joke
    return render_template("index.html", joke=data[index_joke])  # see the main website


@app.route('/register', methods=['GET', 'POST'])  # register
def reqister():
    form = RegisterForm()  # register form
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:  # check password and password_again
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():  # check user in base users
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(  # add user to base users
            name=form.name.data
        )
        user.date_to_sign(form.date.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')  # go to the next website
    return render_template('register.html', title='Регистрация', form=form)  # see the register website


@login_manager.user_loader
def load_user(user_id):  # get user for normal flask-login's work
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])  # login
def login():
    form = LoginForm()  # login form
    if form.validate_on_submit():
        db_sess = db_session.create_session()  # create session
        user = db_sess.query(User).filter(User.name == form.name.data).first()  # find user
        if user and user.check_password(form.password.data):  # check user
            login_user(user, remember=form.remember_me.data) # remember user
            return redirect("/")
        return render_template('login.html',  # error
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)  # see the login website


@app.route('/logout')
@login_required
def logout():  # forget user and go to main website
    logout_user()
    return redirect("/")


@app.route('/horoscope')
@login_required
def horoscope():
    #db_sess = db_session.create_session()
    #user = db_sess.query(User).filter(User.id == current_user.id).first()
    '''if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)'''
    with open('znaki.json') as sign_file:  # open json file
        data = json.load(sign_file)
        about_sign = data[current_user.sign]
    with open('info.json') as info_file:  # open json file
        data = json.load(info_file)
        prediction = data[current_user.sign]
    return render_template('horoscope.html',
                           title='Редактирование новости',
                           name=current_user.name,
                           sign=current_user.sign,
                           # picture=
                           about=about_sign,
                           prediction=prediction)


'''@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('horoscope.html', title='Добавление новости',
                           form=form)'''


'''@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('horoscope.html',
                           title='Редактирование новости',
                           form=form
                           )'''


def main():
    db_session.global_init("db/horoscope.db")
    app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
