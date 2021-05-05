import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.equipment import Equipment
    from wod_board.models.unit import Unit


class MovementEquipment(models.Base):
    __tablename__ = "movement_equipment"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    movement_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("movement.id")
    )
    equipment_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("equipment.id")
    )


class Movement(models.Base):
    __tablename__ = "movement"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)
    unit_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("unit.id"), nullable=False
    )

    unit: "Unit" = sqlalchemy.orm.relationship("Unit")
    equipments: typing.List["Equipment"] = sqlalchemy.orm.relationship(
        "Equipment",
        secondary="movement_equipment",
        lazy="dynamic",
    )
