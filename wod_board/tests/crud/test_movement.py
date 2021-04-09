import pytest

from wod_board.crud import movement_crud
from wod_board.models import movement
from wod_board.schemas import movement_schemas


MOVEMENT_NAME = "Devil Press"


def test_create_movement(db):
    movement_schema = movement_schemas.MovementCreate(name=MOVEMENT_NAME)

    created_movement = movement_crud._create_movement(db, movement_schema)
    assert created_movement.name == movement_schema.name


def test_get_movement_by_exact_name(db):
    movement_schema = movement_schemas.MovementCreate(name=MOVEMENT_NAME)

    db.add(movement.Movement(**movement_schema.dict()))
    db.commit()

    wanted_movement = movement_crud._get_movement_by_exact_name(db, movement_schema)
    assert wanted_movement.name == movement_schema.name

    movement_schema = movement_schemas.MovementCreate(name="Burpee")
    with pytest.raises(movement_crud.UnknownMovement):
        movement_crud._get_movement_by_exact_name(db, movement_schema)


def test_get_or_create_movement(db):
    movement_schema = movement_schemas.MovementCreate(name=MOVEMENT_NAME)

    wanted_movement = movement_crud.get_or_create_movement(db, movement_schema)
    assert wanted_movement.name == movement_schema.name

    wanted_movement = movement_crud.get_or_create_movement(db, movement_schema)
    assert wanted_movement.name == movement_schema.name

    movements = db.query(movement.Movement)
    assert movements.count() == 1
