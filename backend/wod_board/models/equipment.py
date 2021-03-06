import typing

import sqlalchemy

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.unit import Unit


class Equipment(models.Base):
    __tablename__ = "equipment"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name: str = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)
    unit_id: typing.Optional[int] = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("unit.id")
    )

    unit: typing.Optional["Unit"] = sqlalchemy.orm.relationship("Unit")
