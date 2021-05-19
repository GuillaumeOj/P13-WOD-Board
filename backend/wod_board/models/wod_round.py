import typing

import sqlalchemy
import sqlalchemy.orm

from wod_board import models


if typing.TYPE_CHECKING:
    from wod_board.models.goal import Goal


class RoundGoal(models.Base):
    __tablename__ = "round_goal"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    round_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("round.id", ondelete="CASCADE"),
        nullable=False,
    )
    goal_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("goal.id", ondelete="CASCADE"),
        nullable=False,
    )


class Round(models.Base):
    __tablename__ = "round"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    position: int = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    duration_seconds: int = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    repetition: int = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    wod_id: int = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("wod.id", ondelete="CASCADE"),
        nullable=False,
    )
    parent_id: typing.Optional[int] = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("round.id")
    )

    sub_rounds: typing.List[typing.Optional["Round"]] = sqlalchemy.orm.relationship(
        "Round",
        cascade="all, delete",
        backref=sqlalchemy.orm.backref("parent", remote_side=[id]),
        lazy="dynamic",
    )
    goals: typing.List["Goal"] = sqlalchemy.orm.relationship(
        "Goal",
        secondary="round_goal",
        lazy="dynamic",
    )

    __tableargs__ = (
        sqlalchemy.UniqueConstraint(wod_id, position, name="wod_id_position"),
    )
