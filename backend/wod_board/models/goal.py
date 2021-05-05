import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.equipment import Equipment
    from wod_board.models.movement import Movement


class GoalEquipment(models.Base):
    __tablename__ = "goal_equipment"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    goal_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("goal.id"))
    equipment_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("equipment.id")
    )


class Goal(models.Base):
    __tablename__ = "goal"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    movement_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("movement.id")
    )
    round_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("round.id"))
    repetition = sqlalchemy.Column(sqlalchemy.Integer)
    duration_seconds = sqlalchemy.Column(sqlalchemy.Integer)

    movement: "Movement" = sqlalchemy.orm.relationship("Movement")
    equipments: typing.List["Equipment"] = sqlalchemy.orm.relationship(
        "Equipment",
        secondary="goal_equipment",
        lazy="dynamic",
    )
