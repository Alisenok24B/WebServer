import datetime as dt
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(SqlAlchemyBase, UserMixin):  # class user
    __tablename__ = 'users'  # table

    id = sqlalchemy.Column(sqlalchemy.Integer,  # user's id
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # user's name
    hashed_password = sqlalchemy.Column(
        sqlalchemy.String, nullable=False)  # user's hashed password
    sign = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # user's sign
    dates_signs = [((3, 21), (4, 19), 'Овен'),  # list signs with dates
                   ((4, 20), (5, 20), 'Телец'),
                   ((5, 21), (6, 20), 'Близнецы'),
                   ((6, 21), (7, 22), 'Рак'),
                   ((7, 23), (8, 22), 'Лев'),
                   ((8, 22), (9, 22), 'Дева'),
                   ((9, 23), (10, 22), 'Весы'),
                   ((10, 23), (11, 21), 'Скорпион'),
                   ((11, 22), (12, 21), 'Стрелец'),
                   ((12, 22), (1, 19), 'Козерог'),
                   ((1, 20), (2, 18), 'Водолей'),
                   ((2, 19), (3, 20), 'Рыбы'),
                   ]

    def date_to_sign(self, date):  # find sign of user
        for i in self.dates_signs:
            if dt.date(date.year if i[0][0] != 12 else date.year - 1,
                       i[0][0], i[0][1]) <= date <= dt.date(date.year,
                                                            i[1][0], i[1][1]):
                self.sign = i[2]
                break

    def set_password(self, password):  # hash password
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):  # check password
        return check_password_hash(self.hashed_password, password)
