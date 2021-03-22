import sqlalchemy
import sqlalchemy.orm

from wod_board import models


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
        nullable=False,
    )

    rounds = sqlalchemy.orm.relationship("Round", cascade="all, delete")


class WodType(models.Base):
    __tablename__ = "wod_type"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(150), nullable=False)


class Round(models.Base):
    __tablename__ = "round"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    position = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    duration_seconds = sqlalchemy.Column(sqlalchemy.Integer)

    parent_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("round.id"),
    )
    wod_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("wod.id"), nullable=False
    )

    sqlalchemy.UniqueConstraint(wod_id, position, name="wod_id_position")
