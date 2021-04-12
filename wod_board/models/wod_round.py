import sqlalchemy
import sqlalchemy.orm

from wod_board import models
from wod_board.models.equipment import Equipment
from wod_board.models.movement import Movement


class RoundMovement(models.Base):
    __tablename__ = "round_movement"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    round_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("round.id"))
    movement_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("movement.id")
    )
    equipment_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("equipment.id")
    )

    equipment: Equipment = sqlalchemy.orm.relationship(Equipment)


class Round(models.Base):
    __tablename__ = "round"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    position = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    duration_seconds = sqlalchemy.Column(sqlalchemy.Integer)
    wod_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("wod.id"), nullable=False
    )
    parent_round_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("round.id")
    )

    sub_rounds = sqlalchemy.orm.relationship(  # type: ignore[misc]
        "Round",
        cascade="all, delete",
        backref=sqlalchemy.orm.backref("parent", remote_side=[id]),
        lazy="dynamic",
    )
    movements: sqlalchemy.orm.Mapped[Movement] = sqlalchemy.orm.relationship(
        Movement,
        secondary="round_movement",
        lazy="dynamic",
    )

    __tableargs__ = (
        sqlalchemy.UniqueConstraint(wod_id, position, name="wod_id_position"),
    )
