import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


class User(models.Base):
    __tablename__ = "user"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    email: str = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    username: str = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    first_name: typing.Optional[str] = sqlalchemy.Column(sqlalchemy.String)
    last_name: typing.Optional[str] = sqlalchemy.Column(sqlalchemy.String)
    is_admin: bool = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"
