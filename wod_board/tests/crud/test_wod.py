import pytest

from wod_board.crud import wod_crud
from wod_board.models import wod
from wod_board.schemas import wod_schemas


WOD_TYPE = "AMRAP"


def test_create_wod_type(db):
    wod_type_schema = wod_schemas.WodTypeBase(name=WOD_TYPE)

    created_type = wod_crud._create_wod_type(db, wod_type_schema)
    assert created_type.name == wod_type_schema.name


def test_get_wod_type_by_name(db):
    wod_type_schema = wod_schemas.WodTypeBase(name=WOD_TYPE)
    wod_crud._create_wod_type(db, wod_type_schema)

    wod_type = wod_crud._get_wod_type_by_exact_name(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name

    wod_type_schema = wod_schemas.WodTypeBase(name="For Time")
    with pytest.raises(wod_crud.UnknownWodType):
        wod_type = wod_crud._get_wod_type_by_exact_name(db, wod_type_schema)


def test_get_or_create_wod_type(db):
    wod_type_schema = wod_schemas.WodTypeBase(name=WOD_TYPE)

    wod_type = wod_crud.get_or_create_wod_type(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name

    wod_type = wod_crud.get_or_create_wod_type(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name

    wod_types = db.query(wod.WodType).all()
    assert len(wod_types) == 1


def test_create_wod(db):
    wod_type_schema = wod_schemas.WodTypeCreate(name=WOD_TYPE)

    wod_schema = wod_schemas.WodCreate(
        description="Foo WOD", note="", wod_type=wod_type_schema
    )

    new_wod = wod_crud.create_wod(db, wod_schema)

    db_wod = db.query(wod.Wod).first()
    assert db_wod.id == new_wod.id
    assert db_wod.description == new_wod.description
    assert db_wod.note == new_wod.note
    assert db_wod.date == new_wod.date
    assert db_wod.rounds.all() == new_wod.rounds
