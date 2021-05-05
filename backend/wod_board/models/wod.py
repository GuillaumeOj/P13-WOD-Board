import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models
from wod_board.models import user


if typing.TYPE_CHECKING:
    from wod_board.models.wod_round import Round


class WodType(models.Base):
    __tablename__ = "wod_type"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)


class Wod(models.Base):
    __tablename__ = "wod"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    is_complete = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=False
    )
    wod_type_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("wod_type.id")
    )

    wod_type: WodType = sqlalchemy.orm.relationship("WodType")
    author: user.User = sqlalchemy.orm.relationship("User")
    rounds: typing.List["Round"] = sqlalchemy.orm.relationship(
        "Round", cascade="all, delete", backref="wod", lazy="dynamic"
    )

    def __repr__(self):
        return f"<WOD {self.title}> by {self.author}"
