import pytest

from wod_board.crud import wod_crud
from wod_board.models import wod
from wod_board.schemas import wod_schemas


WOD_TYPE = "AMRAP"


def test_create_wod_type(db):
    wod_type_schema = wod_schemas.WodTypeBase(name=WOD_TYPE)

    wod_type = wod_crud.create_wod_type(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name


def test_get_wod_type_by_name(db):
    with pytest.raises(wod_crud.UnknownWodType):
        wod_crud.get_wod_type_by_exact_name(db, WOD_TYPE)

    db.add(wod.WodType(name=WOD_TYPE))
    db.commit()

    wod_type = wod_crud.get_wod_type_by_exact_name(db, WOD_TYPE)
    assert wod_type.name == WOD_TYPE


def test_get_or_create_wod_type(db):
    wod_type_schema = wod_schemas.WodTypeBase(name=WOD_TYPE)

    wod_type = wod_crud.get_or_create_wod_type(db, wod_type_schema)
    assert wod_type.name == WOD_TYPE

    wod_type = wod_crud.get_or_create_wod_type(db, wod_type_schema)
    assert wod_type.name == WOD_TYPE
    assert db.query(wod.WodType).count() == 1


def test_create_wod(db):
    wod_type_schema = wod_schemas.WodTypeCreate(name=WOD_TYPE)

    wod_schema = wod_schemas.WodCreate(wod_type=wod_type_schema)

    new_wod = wod_crud.create_wod(db, wod_schema)
    db_wod = db.query(wod.Wod).first()
    assert db_wod.id == new_wod.id
    assert db_wod.description == new_wod.description
    assert db_wod.note == new_wod.note
    assert db_wod.date == new_wod.date
    assert db_wod.rounds.count() == new_wod.rounds.count()


def test_update_wod(db):
    db_wod_type = wod.WodType(name=WOD_TYPE)
    db_wod = wod.Wod(note="Bad Note", wod_type=db_wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    wod_type_schema = wod_schemas.WodTypeCreate(name=WOD_TYPE)
    wod_schema = wod_schemas.WodCreate(note="Correct Note", wod_type=wod_type_schema)

    assert db_wod.note != wod_schema.note

    wod_crud.update_wod(db, wod_schema, db_wod.id)
    db_wod = db.get(wod.Wod, db_wod.id)
    assert db_wod.note == wod_schema.note

    with pytest.raises(wod_crud.UnknownWod):
        wod_crud.update_wod(db, wod_schema, 2)


def test_get_wod_by_id(db):
    with pytest.raises(wod_crud.UnknownWod):
        wod_crud.get_wod_by_id(db, 1)

    wanted_wod = wod.Wod()
    db.add(wanted_wod)
    db.commit()

    wanted_wod = wod_crud.get_wod_by_id(db, 1)
    assert wanted_wod.id == 1
