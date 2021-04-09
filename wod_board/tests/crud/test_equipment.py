import pytest

from wod_board.crud import equipment_crud
from wod_board.models import equipment
from wod_board.schemas import equipment_schemas


EQUIPMENT_NAME = "Dumbbel"


def test_create_equipment(db):
    equipment_schema = equipment_schemas.EquipmentCreate(name=EQUIPMENT_NAME)

    created_equipment = equipment_crud._create_equipment(db, equipment_schema)
    assert created_equipment.name == equipment_schema.name


def test_get_equipment_by_exact_name(db):
    equipment_schema = equipment_schemas.EquipmentCreate(name=EQUIPMENT_NAME)

    db.add(equipment.Equipment(**equipment_schema.dict()))
    db.commit()

    wanted_equipment = equipment_crud._get_equipment_by_exact_name(db, equipment_schema)
    assert wanted_equipment.name == equipment_schema.name

    equipment_schema = equipment_schemas.EquipmentCreate(name="Barbell")
    with pytest.raises(equipment_crud.UnknownEquipment):
        equipment_crud._get_equipment_by_exact_name(db, equipment_schema)


def test_get_or_create_equipment(db):
    equipment_schema = equipment_schemas.EquipmentCreate(name=EQUIPMENT_NAME)

    new_equipment = equipment_crud.get_or_create_equipment(db, equipment_schema)
    assert new_equipment.name == equipment_schema.name

    new_equipment = equipment_crud.get_or_create_equipment(db, equipment_schema)
    assert new_equipment.name == equipment_schema.name

    equipments = db.query(equipment.Equipment)
    assert equipments.count() == 1


def test_get_or_create_equipments(db):
    dumbbel_schema = equipment_schemas.EquipmentCreate(name="Dumbbel")
    barbell_schema = equipment_schemas.EquipmentCreate(name="Barbell")

    equipments = equipment_crud.get_or_create_equipments(
        db, [dumbbel_schema, barbell_schema]
    )
    assert len(equipments) == 2
