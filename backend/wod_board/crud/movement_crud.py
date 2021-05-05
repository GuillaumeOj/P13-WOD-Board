import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import movement
from wod_board.schemas import movement_schemas


LOG = daiquiri.getLogger(__name__)


def create_movement(
    db: sqlalchemy.orm.Session,
    movement_data: movement_schemas.MovementCreate,
) -> movement.Movement:
    new_movement = movement.Movement(
        name=movement_data.name, unit_id=movement_data.unit_id
    )
    db.add(new_movement)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'insert or update on table "movement" violates foreign '
            'key constraint "movement_unit_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownUnit
        if (
            'duplicate key value violates unique constraint "movement_name_key"'
        ) in str(error):
            raise exceptions.DuplicatedMovement

        LOG.error(str(error))

    db.refresh(new_movement)

    return new_movement


def get_movement_by_id(
    db: sqlalchemy.orm.Session,
    id: int,
) -> movement.Movement:
    db_movement: movement.Movement = db.get(movement.Movement, id)

    if db_movement is None:
        raise exceptions.UnknownMovement

    return db_movement


def get_movement_by_name(
    db: sqlalchemy.orm.Session,
    name: str,
) -> movement.Movement:
    db_movement: typing.Optional[movement.Movement] = (
        db.query(movement.Movement).filter(movement.Movement.name == name).first()
    )

    if db_movement is None:
        raise exceptions.UnknownMovement

    return db_movement


def get_or_create_movement(
    db: sqlalchemy.orm.Session,
    movement_data: movement_schemas.MovementCreate,
) -> movement.Movement:
    try:
        db_movement = get_movement_by_name(db, movement_data.name)
    except exceptions.UnknownMovement:
        db_movement = create_movement(db, movement_data)

    return db_movement


def get_movements_by_name(
    db: sqlalchemy.orm.Session,
    name: str,
) -> typing.List[typing.Optional[movement.Movement]]:
    movements: typing.List[typing.Optional[movement.Movement]] = (
        db.query(movement.Movement)
        .filter(movement.Movement.name.ilike(f"%{name}%"))
        .all()
    )

    return movements
