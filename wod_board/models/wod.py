import datetime
import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


class WodType(models.Base):
    __tablename__ = "wod_type"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(150), nullable=False, unique=True)

    def __init__(self, name: str):
        self.name = name


class Wod(models.Base):
    __tablename__ = "wod"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    note = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()
    )
    wod_type_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("wod_type.id"),
        nullable=False,
    )

    wod_type = sqlalchemy.orm.relationship("WodType")  # type: ignore[misc]
    rounds = sqlalchemy.orm.relationship(  # type: ignore[misc]
        "Round", cascade="all, delete", backref="wod", lazy="dynamic"
    )

    def __init__(
        self,
        wod_type_id: int,
        description: typing.Optional[str] = None,
        note: typing.Optional[str] = None,
        date: datetime.datetime = datetime.datetime.utcnow(),
    ):
        self.wod_type_id = wod_type_id
        self.description = description
        self.note = note
        self.date = date
