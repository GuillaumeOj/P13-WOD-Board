import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.equipment import Equipment
    from wod_board.models.unit import Unit


class MovementEquipment(models.Base):
    __tablename__ = "movement_equipment"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    movement_id: int = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("movement.id", ondelete="CASCADE"),
        nullable=False,
    )
    equipment_id: int = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("equipment.id", ondelete="CASCADE"),
        nullable=False,
    )


class Movement(models.Base):
    __tablename__ = "movement"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name: str = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)
    unit_id: int = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("unit.id")
    )

    unit: "Unit" = sqlalchemy.orm.relationship("Unit")
    equipments: typing.List[typing.Optional["Equipment"]] = sqlalchemy.orm.relationship(
        "Equipment",
        secondary="movement_equipment",
        lazy="dynamic",
    )
