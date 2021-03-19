import sqlalchemy

from wod_board import models


class Round(models.Base):
    __tablename__ = "wod_board_round"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    position = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    duration_seconds = sqlalchemy.Column(sqlalchemy.Integer)

    parent_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("wod_board_round.id"),
    )
    wod_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("wod_board_wod.id"), nullable=False
    )

    sqlalchemy.UniqueConstraint(wod_id, position, name="wod_id_position")
