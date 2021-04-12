import pydantic
import sqlalchemy.orm

from wod_board.crud import equipment_crud
from wod_board.crud import unit_crud
from wod_board.models import movement
from wod_board.schemas import movement_schemas


class UnknownMovement(Exception):
    pass


def create_movement(
    db: sqlalchemy.orm.Session,
    movement_data: movement_schemas.MovementCreate,
) -> movement.Movement:
    new_movement = movement.Movement(name=movement_data.name)

    if movement_data.equipments:
        new_movement.equipments = [
            equipment_crud.get_or_create_equipment(db, equipment)
            for equipment in movement_data.equipments
        ]

    if movement_data.unit:
        new_movement.unit = unit_crud.get_or_create_unit(db, movement_data.unit)

    db.add(new_movement)

    db.commit()
    db.refresh(new_movement)

    return new_movement


def get_movement_by_id(
    db: sqlalchemy.orm.Session,
    id: int,
) -> movement.Movement:
    db_movement: movement.Movement = db.get(movement.Movement, id)

    if db_movement is None:
        raise UnknownMovement

    return db_movement


def get_movement_by_exact_name(
    db: sqlalchemy.orm.Session,
    name: str = pydantic.Field(..., max_length=250),
) -> movement.Movement:
    db_movement: movement.Movement = (
        db.query(movement.Movement).filter(movement.Movement.name == name).first()
    )

    if db_movement is None:
        raise UnknownMovement

    return db_movement


def get_or_create_movement(
    db: sqlalchemy.orm.Session,
    movement_data: movement_schemas.MovementCreate,
) -> movement.Movement:
    try:
        db_movement = get_movement_by_exact_name(db, movement_data.name)
    except UnknownMovement:
        db_movement = create_movement(db, movement_data)

    return db_movement
