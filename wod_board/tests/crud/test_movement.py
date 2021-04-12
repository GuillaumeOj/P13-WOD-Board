import pytest

from wod_board.crud import movement_crud
from wod_board.models import equipment
from wod_board.models import movement
from wod_board.models import unit
from wod_board.schemas import equipment_schemas
from wod_board.schemas import movement_schemas
from wod_board.schemas import unit_schemas


def test_create_movement(db):
    devil_press = movement_schemas.MovementCreate(name="Devil Press")

    created_movement = movement_crud.create_movement(db, devil_press)
    assert created_movement.name == devil_press.name


def test_get_movement_by_id(db):
    with pytest.raises(movement_crud.UnknownMovement):
        movement_crud.get_movement_by_id(db, 1)

    devil_press = movement_schemas.MovementCreate(name="Devil Press")
    db.add(movement.Movement(name=devil_press.name))
    db.commit()

    db_devil_press = movement_crud.get_movement_by_id(db, 1)
    assert db_devil_press.name == devil_press.name


def test_get_movement_by_exact_name(db):
    devil_press = movement_schemas.MovementCreate(name="Devil Press")

    db.add(movement.Movement(name=devil_press.name))
    db.commit()

    devil_press = movement_crud.get_movement_by_exact_name(db, devil_press.name)
    assert devil_press.name == devil_press.name

    with pytest.raises(movement_crud.UnknownMovement):
        movement_crud.get_movement_by_exact_name(db, "Burpee")


def test_get_or_create_movement(db):
    dumbbel_schema = equipment_schemas.EquipmentCreate(name="Dumbbel")
    barbell_schema = equipment_schemas.EquipmentCreate(name="Barbell")
    equipments = [dumbbel_schema, barbell_schema]
    unit_unit = unit_schemas.UnitCreate(name="Unit", symbol="u")

    devil_press = movement_schemas.MovementCreate(
        name="Devil Press", equipments=equipments, unit=unit_unit
    )

    wanted_movement = movement_crud.get_or_create_movement(db, devil_press)
    db_equipments = db.query(equipment.Equipment).all()
    db_unit = db.query(unit.Unit).first()
    assert wanted_movement.name == devil_press.name
    assert wanted_movement.unit == db_unit
    assert wanted_movement.equipments.all() == db_equipments

    wanted_movement = movement_crud.get_or_create_movement(db, devil_press)
    movements = db.query(movement.Movement)
    assert wanted_movement.name == devil_press.name
    assert movements.count() == 1
