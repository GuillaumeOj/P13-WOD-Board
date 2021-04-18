import sqlalchemy
import sqlalchemy.orm

from wod_board import models


class Unit(models.Base):
    __tablename__ = "unit"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)
    symbol = sqlalchemy.Column(sqlalchemy.String(5), nullable=False)

    __tableargs__ = sqlalchemy.UniqueConstraint(name, symbol, name="name_symbol")
