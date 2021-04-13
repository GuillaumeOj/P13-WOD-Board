import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.wod_round import Round


class WodType(models.Base):
    __tablename__ = "wod_type"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(150), nullable=False, unique=True)


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
    )

    wod_type: WodType = sqlalchemy.orm.relationship("WodType")
    rounds: typing.List["Round"] = sqlalchemy.orm.relationship(
        "Round", cascade="all, delete", backref="wod", lazy="dynamic"
    )
