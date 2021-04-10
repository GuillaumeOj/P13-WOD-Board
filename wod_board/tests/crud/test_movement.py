import pytest

from wod_board.crud import movement_crud
from wod_board.models import equipment
from wod_board.models import movement
from wod_board.schemas import equipment_schemas
from wod_board.schemas import movement_schemas


def test_create_movement(db):
    movement_schema = movement_schemas.MovementCreate(name="Devil Press")

    created_movement = movement_crud._create_movement(db, movement_schema)
    assert created_movement.name == movement_schema.name


def test_get_movement_by_exact_name(db):
    movement_schema = movement_schemas.MovementCreate(name="Devil Press")

    db.add(movement.Movement(**movement_schema.dict()))
    db.commit()

    wanted_movement = movement_crud.get_movement_by_exact_name(db, movement_schema.name)
    assert wanted_movement.name == movement_schema.name

    with pytest.raises(movement_crud.UnknownMovement):
        movement_crud.get_movement_by_exact_name(db, "Burpee")


def test_get_or_create_movement(db):
    dumbbel_schema = equipment_schemas.EquipmentCreate(name="Dumbbel")
    barbell_schema = equipment_schemas.EquipmentCreate(name="Barbell")
    equipments = [dumbbel_schema, barbell_schema]

    movement_schema = movement_schemas.MovementCreate(
        name="Devil Press", equipments=equipments
    )

    wanted_movement = movement_crud.get_or_create_movement(db, movement_schema)
    assert wanted_movement.name == movement_schema.name

    db_equipments = db.query(equipment.Equipment).all()
    assert wanted_movement.equipments == [
        equipment_schemas.Equipment.from_orm(db_equipment)
        for db_equipment in db_equipments
    ]

    wanted_movement = movement_crud.get_or_create_movement(db, movement_schema)
    assert wanted_movement.name == movement_schema.name

    movements = db.query(movement.Movement)
    assert movements.count() == 1
