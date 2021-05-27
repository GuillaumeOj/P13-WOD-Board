import datetime

import pytest

from wod_board import exceptions
from wod_board.crud import wod_crud
from wod_board.models import wod
from wod_board.schemas import wod_schemas


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
            is_complete=False,
            author_id=db_user.id,
            date=datetime.datetime.utcnow(),
        )
    )
    db.commit()
    assert db.query(wod.Wod).count() == 2

    wod_schema = wod_schemas.WodCreate(
        title="Karen", author_id=db_user.id, is_complete=True
    )
    assert db_wod.title != wod_schema.title

    assert wod_crud.update_wod(db, wod_schema, db_wod.id)

    db.refresh(db_wod)
    assert db_wod.title == wod_schema.title
    assert db_wod.is_complete == wod_schema.is_complete
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


def test_get_wod_incomplete(db, db_user, db_wod):
    db.add(
        wod.Wod(
            title="Dummy WOD",
            date=datetime.datetime.utcnow(),
            is_complete=True,
            author_id=db_user.id,
        )
    )
    db.commit()
    assert db.query(wod.Wod).count() == 2
    assert not db_wod.is_complete
    assert db_wod.author_id == db_user.id

    uncomplete_wod = wod_crud.get_wod_incomplete(db, db_user.id)
    assert isinstance(uncomplete_wod, wod.Wod)
    assert uncomplete_wod.id == db_wod.id
