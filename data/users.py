import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    university = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    faculty = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    delta = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    olymps_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    achiv = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    #university = orm.relationship('University')