import datetime

import pytest

from wod_board import exceptions
from wod_board.crud import wod_crud
from wod_board.models import wod
from wod_board.schemas import wod_schemas


WOD_TYPE = "AMRAP"


def test_create_wod_type(db):
    wod_type_schema = wod_schemas.WodTypeCreate(name=WOD_TYPE)

    wod_type = wod_crud.create_wod_type(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name


def test_get_wod_type_by_name(db):
    with pytest.raises(exceptions.UnknownWodType):
        wod_crud.get_wod_type_by_name(db, WOD_TYPE)

    db.add(wod.WodType(name=WOD_TYPE))
    db.commit()

    wod_type = wod_crud.get_wod_type_by_name(db, WOD_TYPE)
    assert wod_type.name == WOD_TYPE


def test_get_wod_types_by_name(db):
    db.add(wod.WodType(name="For Time"))
    db.add(wod.WodType(name="For Load"))
    db.commit()

    wod_types = wod_crud.get_wod_types_by_name(db, "for")
    assert len(wod_types) == 2

    wod_types = wod_crud.get_wod_types_by_name(db, "loa")
    assert len(wod_types) == 1


def test_get_wod_type_all(db):
    wod_types = wod_crud.get_wod_type_all(db)
    assert len(wod_types) == 0

    db.add(wod.WodType(name=WOD_TYPE))
    db.commit()

    wod_types = wod_crud.get_wod_type_all(db)
    assert len(wod_types) == 1


def test_get_or_create_wod_type(db):
    wod_type_schema = wod_schemas.WodTypeCreate(name=WOD_TYPE)

    wod_type = wod_crud.get_or_create_wod_type(db, wod_type_schema)
    assert wod_type.name == WOD_TYPE

    wod_type = wod_crud.get_or_create_wod_type(db, wod_type_schema)
    assert wod_type.name == WOD_TYPE
    assert db.query(wod.WodType).count() == 1


def test_create_wod(db, db_user):
    wod_schema = wod_schemas.WodCreate(
        title="Murph",
        wod_type_id=1,
        author_id=db_user.id,
        date=datetime.datetime.utcnow(),
    )
    with pytest.raises(exceptions.UnknownWodType):
        wod_crud.create_wod(db, wod_schema)

    wod_schema = wod_schemas.WodCreate(title="Murph", author_id=2)
    with pytest.raises(exceptions.UnknownUser):
        wod_crud.create_wod(db, wod_schema)

    assert db.query(wod.Wod).count() == 0

    wod_schema = wod_schemas.WodCreate(title="Murph", author_id=db_user.id)

    assert wod_crud.create_wod(db, wod_schema)
    assert db.query(wod.Wod).count() == 1

    with pytest.raises(exceptions.TitleAlreadyUsed):
        wod_crud.create_wod(db, wod_schema)

    assert db.query(wod.Wod).count() == 1


def test_update_wod(db, db_user, db_wod):
    db.add(
        wod.Wod(
            title="Cindy",
            is_complete=True,
            author_id=db_user.id,
            date=datetime.datetime.utcnow(),
        )
    )
    db.commit()
    assert db.query(wod.Wod).count() == 2

    wod_schema = wod_schemas.WodCreate(title="Karen", author_id=db_user.id)
    assert db_wod.title != wod_schema.title

    assert wod_crud.update_wod(db, wod_schema, db_wod.id)

    db.refresh(db_wod)
    assert db_wod.title == wod_schema.title
    assert db.query(wod.Wod).count() == 2

    with pytest.raises(exceptions.UnknownWod):
        wod_crud.update_wod(db, wod_schema, 3)

    wod_schema = wod_schemas.WodCreate(title="Karen", author_id=2)
    with pytest.raises(exceptions.UnknownUser):
        wod_crud.update_wod(db, wod_schema, db_wod.id)

    wod_schema = wod_schemas.WodCreate(title="Cindy", author_id=db_user.id)
    with pytest.raises(exceptions.TitleAlreadyUsed):
        wod_crud.update_wod(db, wod_schema, db_wod.id)

    assert db.query(wod.Wod).count() == 2


def test_get_wod_by_id(db, db_wod):
    with pytest.raises(exceptions.UnknownWod):
        wod_crud.get_wod_by_id(db, 2)

    wanted_wod = wod_crud.get_wod_by_id(db, db_wod.id)
    assert wanted_wod.title == db_wod.title
