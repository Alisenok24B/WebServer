import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):  # class user
    __tablename__ = 'users'  # table

    id = sqlalchemy.Column(sqlalchemy.Integer,  # user's id
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # user's name
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)  # user's date of birth
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # user's hashed password
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # created date of this user
    news = orm.relation("News", back_populates='user')  # will be change when I will understand how

    def __repr__(self):  # str data if user
        return f'''<User> {self.id} {self.name} {self.date}'''

    def set_password(self, password):  # hash password
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):  # check password
        return check_password_hash(self.hashed_password, password)
