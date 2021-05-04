import pytest

from wod_board import exceptions
from wod_board.crud import unit_crud
from wod_board.models import unit
from wod_board.schemas import unit_schemas


UNIT_NAME = "Kilograms"
UNIT_SYMBOL = "kg"


def test_create_unit(db):
    unit_schema = unit_schemas.UnitCreate(name=UNIT_NAME, symbol=UNIT_SYMBOL)

    created_unit = unit_crud._create_unit(db, unit_schema)
    assert created_unit.name == unit_schema.name
    assert created_unit.symbol == unit_schema.symbol


def test_get_unit_by_exact_name(db):
    unit_schema = unit_schemas.UnitCreate(name=UNIT_NAME, symbol=UNIT_SYMBOL)

    db.add(unit.Unit(**unit_schema.dict()))
    db.commit()

    wanted_unit = unit_crud.get_unit_by_exact_name(db, unit_schema.name)
    assert wanted_unit.name == unit_schema.name
    assert wanted_unit.symbol == unit_schema.symbol

    with pytest.raises(exceptions.UnknownUnit):
        unit_crud.get_unit_by_exact_name(db, "Unit")


def test_get_or_create_unit(db):
    unit_schema = unit_schemas.UnitCreate(name=UNIT_NAME, symbol=UNIT_SYMBOL)

    new_unit = unit_crud.get_or_create_unit(db, unit_schema)
    assert new_unit.name == unit_schema.name
    assert new_unit.symbol == unit_schema.symbol

    new_unit = unit_crud.get_or_create_unit(db, unit_schema)
    assert new_unit.name == unit_schema.name
    assert new_unit.symbol == unit_schema.symbol

    units = db.query(unit.Unit)
    assert units.count() == 1
