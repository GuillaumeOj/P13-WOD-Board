import sqlalchemy
import sqlalchemy.orm

from wod_board import models


class Round(models.Base):
    __tablename__ = "round"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    position = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    duration_seconds = sqlalchemy.Column(sqlalchemy.Integer)
    wod_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("wod.id"), nullable=False
    )
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("round.id"))

    children = sqlalchemy.orm.relationship(  # type: ignore[misc]
        "Round",
        cascade="all, delete",
        backref=sqlalchemy.orm.backref("parent", remote_side=[id]),
        lazy="dynamic",
    )

    __tableargs__ = (
        sqlalchemy.UniqueConstraint(wod_id, position, name="wod_id_position"),
    )
