import sqlalchemy
import sqlalchemy.orm

from wod_board import models


class MovementEquipment(models.Base):
    __tablename__ = "movement_equipment"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    movement_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("movement.id")
    )
    equipment_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("equipment.id")
    )


class Movement(models.Base):
    __tablename__ = "movement"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)
    unit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("unit.id"))

    equipments = sqlalchemy.orm.relationship(  # type: ignore[misc]
        "Equipment",
        secondary="movement_equipment",
        lazy="dynamic",
    )
