# WebServer "Гороскоп"
Project of Yandex.Lyceum WebServer

Задача: выдавать предсказания и немного информации о знаке задиака зарегистрированных пользователей

Инструкция по эксплуатации:
1. Главная страница: можно зарегистрироваться или войти в уже существующий аккаунт, а также увидеть забавные факты о гороскопе
2. Регистрация: необходимо ввести свое имя, дату рождения, пароль и подтверждающий пароль (после чего попадаете на страницу авторизации)
3. Авторизация: необходимо ввести свое имя и пароль
4. Страница с гороскопом: краткое описание знака зодиака, предсказание на день и картинка знака
Примечание: если авторизированный пользователь не вышел из своего аккаунта, главная страница автоматически перебросит в гороскоп
            чтобы выйти со страницы гороскопа на главную необходимо ткнуть на иконку со своим именем в правом верхнем углу

Структура проекта:
app:
* data: __all_models.py - хранит модели для работы с базой данных
        db_session.py - подключение к базе данных и создание сессии для работы с ней
        users.py - содержит класс User — модель для работы с таблицей, содержащей информацию о пользователях
* db: horoscope.db - база данных
* forms: user.py - содержит классы регистрации и авторизации
* static:
  * img - картинки
  * json: signs.json - описание знаков
          info.json - предсказания
          about_horoscope.json - факты о гороскопе
* templates: base.html - базовый шаблон
             index.html - шаблон главной страницы
             horoscope.html - шаблон страницы с личным гороскопом
             login.html - шаблон авторизации
             register.html - шаблон регистрации
* main.py - запускаемый файл

README.md - краткое описание проекта и примечания
requirements.txt - необходимые установки перед эксплуатацией

Использованные технологии:
* SQL база
* SqlAlchemy
* Flask, flask-login, flask-wtf
* Json файлы
* css