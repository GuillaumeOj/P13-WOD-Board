import pytest

from wod_board.crud import equipment_crud
from wod_board.models import equipment
from wod_board.schemas import equipment_schemas


EQUIPMENT_NAME = "Dumbbell"


def test_create_equipment(db):
    dumbbell = equipment_schemas.EquipmentCreate(name=EQUIPMENT_NAME)

    db_dumbbell = equipment_crud.create_equipment(db, dumbbell)
    assert db_dumbbell.name == dumbbell.name


def test_get_equipment_by_exact_name(db):
    with pytest.raises(equipment_crud.UnknownEquipment):
        equipment_crud.get_equipment_by_exact_name(db, EQUIPMENT_NAME)

    dumbbell = equipment_schemas.EquipmentCreate(name=EQUIPMENT_NAME)

    db.add(equipment.Equipment(name=dumbbell.name))
    db.commit()

    db_dumbbell = equipment_crud.get_equipment_by_exact_name(db, dumbbell.name)
    assert db_dumbbell.name == dumbbell.name


def test_get_or_create_equipment(db):
    dumbbell = equipment_schemas.EquipmentCreate(name=EQUIPMENT_NAME)

    db_dumbbell = equipment_crud.get_or_create_equipment(db, dumbbell)
    assert db_dumbbell.name == dumbbell.name

    equipment_crud.get_or_create_equipment(db, dumbbell)
    equipments = db.query(equipment.Equipment)
    assert equipments.count() == 1
