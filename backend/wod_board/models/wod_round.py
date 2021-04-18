import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.movement import MovementGoal


class RoundMovement(models.Base):
    __tablename__ = "round_movement_goal"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    round_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("round.id"))
    movement_goal_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("movement_goal.id")
    )


class Round(models.Base):
    __tablename__ = "round"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    position = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    duration_seconds = sqlalchemy.Column(sqlalchemy.Integer)
    wod_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("wod.id"))
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("round.id"))

    sub_rounds: typing.List["Round"] = sqlalchemy.orm.relationship(
        "Round",
        cascade="all, delete",
        backref=sqlalchemy.orm.backref("parent", remote_side=[id]),
        lazy="dynamic",
    )
    movements: typing.List["MovementGoal"] = sqlalchemy.orm.relationship(
        "MovementGoal",
        secondary="round_movement_goal",
        lazy="dynamic",
    )

    __tableargs__ = (
        sqlalchemy.UniqueConstraint(wod_id, position, name="wod_id_position"),
    )
