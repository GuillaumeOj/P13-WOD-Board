import pytest

from wod_board import exceptions
from wod_board.crud import equipment_crud
from wod_board.models import equipment
from wod_board.schemas import equipment_schemas


EQUIPMENT_NAME = "Dumbbell"


def test_create_equipment(db):
    assert db.query(equipment.Equipment).count() == 0

    dumbbell = equipment_schemas.EquipmentCreate(name=EQUIPMENT_NAME)
    assert equipment_crud.create_equipment(db, dumbbell)
    assert db.query(equipment.Equipment).count() == 1

    with pytest.raises(exceptions.NameAlreadyUsed):
        equipment_crud.create_equipment(db, dumbbell)
    assert db.query(equipment.Equipment).count() == 1


def test_get_equipment_by_name(db):
    assert db.query(equipment.Equipment).count() == 0
    with pytest.raises(exceptions.UnknownEquipment):
        equipment_crud.get_equipment_by_name(db, EQUIPMENT_NAME)

    dumbbell = equipment_schemas.EquipmentCreate(name=EQUIPMENT_NAME)
    db.add(equipment.Equipment(name=dumbbell.name))
    db.commit()
    assert db.query(equipment.Equipment).count() == 1

    db_dumbbell = equipment_crud.get_equipment_by_name(db, dumbbell.name)
    assert db_dumbbell.name == dumbbell.name
