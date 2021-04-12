import typing

import pydantic
import sqlalchemy.orm

from wod_board.crud import equipment_crud
from wod_board.models import movement
from wod_board.schemas import movement_schemas


class UnknownMovement(Exception):
    pass


def _create_movement(
    db: sqlalchemy.orm.Session,
    movement_schema: movement_schemas.MovementCreate,
) -> movement.Movement:
    new_movement = movement.Movement(**movement_schema.dict())

    if movement_schema.equipments:
        new_movement.equipments = (
            equipment_crud.get_or_create_equipments(  # type: ignore[assignment]
                db, movement_schema.equipments
            )
        )

    db.add(new_movement)

    db.commit()
    db.refresh(new_movement)

    return new_movement


def get_movement_by_id(
    db: sqlalchemy.orm.Session,
    id: int,
) -> movement.Movement:
    db_movement: typing.Optional[movement.Movement] = db.get(movement.Movement, id)

    if db_movement is None:
        raise UnknownMovement

    return db_movement


def get_movement_by_exact_name(
    db: sqlalchemy.orm.Session,
    name: str = pydantic.Field(..., max_length=250),
) -> movement.Movement:
    db_movement: typing.Optional[movement.Movement] = (
        db.query(movement.Movement).filter(movement.Movement.name == name).first()
    )

    if db_movement is None:
        raise UnknownMovement

    return db_movement


def get_or_create_movement(
    db: sqlalchemy.orm.Session,
    wanted_movement: movement_schemas.MovementCreate,
) -> movement.Movement:
    try:
        db_movement = get_movement_by_exact_name(db, wanted_movement.name)
    except UnknownMovement:
        db_movement = _create_movement(db, wanted_movement)

    return db_movement
