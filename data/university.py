import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class University(SqlAlchemyBase):
    __tablename__ = 'university'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    faculty = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    olymps_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subjects = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    #user = orm.relationship("User", back_populates='users')