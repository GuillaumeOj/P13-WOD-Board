import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.equipment import Equipment
    from wod_board.models.movement import Movement


class GoalEquipment(models.Base):
    __tablename__ = "goal_equipment"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    goal_id: int = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("goal.id"), nullable=False
    )
    equipment_id: int = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("equipment.id"), nullable=False
    )


class Goal(models.Base):
    __tablename__ = "goal"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    movement_id: int = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("movement.id"), nullable=False
    )
    round_id: int = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("round.id"), nullable=False
    )
    repetition: typing.Optional[int] = sqlalchemy.Column(sqlalchemy.Integer)
    duration_seconds: typing.Optional[int] = sqlalchemy.Column(sqlalchemy.Integer)

    movement: "Movement" = sqlalchemy.orm.relationship("Movement")
    equipments: typing.List[typing.Optional["Equipment"]] = sqlalchemy.orm.relationship(
        "Equipment",
        secondary="goal_equipment",
        lazy="dynamic",
    )
