import sqlalchemy
import sqlalchemy.orm

from wod_board import models


class Wod(models.Base):
    __tablename__ = "wod_board_wod"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    note = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()
    )

    wod_type_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("wod_board_wod_type.id"),
        nullable=False,
    )
    wod_type = sqlalchemy.orm.relationship("WodType", back_populates="wods")


class WodType(models.Base):
    __tablename__ = "wod_board_wod_type"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(150), nullable=False)

    wods = sqlalchemy.orm.relationship("Wod", back_populates="wod_type")
