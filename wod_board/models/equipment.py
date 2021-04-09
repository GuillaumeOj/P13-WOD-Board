import sqlalchemy

from wod_board import models


class Equipment(models.Base):
    __tablename__ = "equipment"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)
    unit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("unit.id"))
