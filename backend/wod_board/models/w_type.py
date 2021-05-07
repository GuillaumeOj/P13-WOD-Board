import sqlalchemy
import sqlalchemy.orm

from wod_board import models


class WodType(models.Base):
    __tablename__ = "wod_type"

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name: str = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)
