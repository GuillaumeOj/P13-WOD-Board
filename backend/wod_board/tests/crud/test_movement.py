import pytest

from wod_board import exceptions
from wod_board.crud import movement_crud
from wod_board.models import movement
from wod_board.models import unit
from wod_board.schemas import movement_schemas


def test_create_movement(db, db_unit):
    assert db.query(movement.Movement).count() == 0

    devil_press = movement_schemas.MovementCreate(
        name="Devil Press", unit_id=db_unit.id
    )
    assert movement_crud.create_movement(db, devil_press)
    assert db.query(movement.Movement).count() == 1

    with pytest.raises(exceptions.DuplicatedMovement):
        movement_crud.create_movement(db, devil_press)
    assert db.query(movement.Movement).count() == 1

    burpees = movement_schemas.MovementCreate(name="Burpees", unit_id=2)
    with pytest.raises(exceptions.UnknownUnit):
        movement_crud.create_movement(db, burpees)


def test_get_movement_by_id(db, db_movement):
    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_id(db, 2)

    wanted_movement = movement_crud.get_movement_by_id(db, db_movement.id)
    assert wanted_movement.id == db_movement.id


def test_get_movement_by_name(db, db_movement):
    devil_press = movement_crud.get_movement_by_name(db, db_movement.name)
    assert devil_press.name == devil_press.name

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_name(db, "Burpee")

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_name(db, db_movement.name.lower())


def test_get_or_create_movement(db):
    unit_unit = unit.Unit(name="Unit", symbol="u")
    db.add(unit_unit)
    db.commit()
    db.refresh(unit_unit)

    assert db.query(movement.Movement).count() == 0

    devil_press = movement_schemas.MovementCreate(
        name="Devil Press", unit_id=unit_unit.id
    )

    assert movement_crud.get_or_create_movement(db, devil_press)
    assert movement_crud.get_or_create_movement(db, devil_press)
    assert db.query(movement.Movement).count() == 1


def test_get_movements_by_name(db, db_unit):
    devil_press = movement.Movement(name="Devil Press", unit_id=db_unit.id)
    push_press = movement.Movement(name="Push Press", unit_id=db_unit.id)
    db.add_all([devil_press, push_press])
    db.commit()
    db.refresh(devil_press)
    db.refresh(push_press)

    movements = movement_crud.get_movements_by_name(db, "pres")
    assert len(movements) == 2

    movements = movement_crud.get_movements_by_name(db, "push pres")
    assert len(movements) == 1
    assert hasattr(movements[0], "name")
    assert movements[0].name == push_press.name

    movements = movement_crud.get_movements_by_name(db, "Burpee")
    assert movements == []
