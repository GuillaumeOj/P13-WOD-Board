import pytest

from wod_board import exceptions
from wod_board.crud import type_crud
from wod_board.models import w_type
from wod_board.schemas import type_schemas


WOD_TYPE = "AMRAP"


def test_create_wod_type(db):
    wod_type_schema = type_schemas.WodTypeCreate(name=WOD_TYPE)
    wod_type = type_crud.create_wod_type(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name

    with pytest.raises(exceptions.NameAlreadyUsed):
        type_crud.create_wod_type(db, wod_type_schema)


def test_get_wod_type_by_name(db):
    with pytest.raises(exceptions.UnknownWodType):
        type_crud.get_wod_type_by_name(db, WOD_TYPE)

    db.add(w_type.WodType(name=WOD_TYPE))
    db.commit()

    wod_type = type_crud.get_wod_type_by_name(db, WOD_TYPE)
    assert wod_type.name == WOD_TYPE


def test_get_wod_types_by_name(db):
    db.add(w_type.WodType(name="For Time"))
    db.add(w_type.WodType(name="For Load"))
    db.commit()

    wod_types = type_crud.get_wod_types_by_name(db, "for")
    assert len(wod_types) == 2

    wod_types = type_crud.get_wod_types_by_name(db, "loa")
    assert len(wod_types) == 1
