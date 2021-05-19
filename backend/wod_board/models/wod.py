import datetime
import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.user import User
    from wod_board.models.w_type import WodType
    from wod_board.models.wod_round import Round


class Wod(models.Base):
    __tablename__ = "wod"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title: str = sqlalchemy.Column(sqlalchemy.String(250), unique=True, nullable=False)
    description: typing.Optional[str] = sqlalchemy.Column(sqlalchemy.String(250))
    date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    is_complete: bool = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    author_id: int = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    wod_type_id: typing.Optional[int] = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("wod_type.id")
    )

    wod_type: typing.Optional["WodType"] = sqlalchemy.orm.relationship("WodType")
    author: "User" = sqlalchemy.orm.relationship("User")
    rounds: typing.List["Round"] = sqlalchemy.orm.relationship(
        "Round", cascade="all, delete", backref="wod", lazy="dynamic"
    )

    def __repr__(self):
        return f"<WOD {self.title}> by {self.author}"
