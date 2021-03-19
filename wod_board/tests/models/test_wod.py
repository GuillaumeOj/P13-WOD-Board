import datetime

import pytest
import sqlalchemy.exc

from wod_board.models import wod


WOD_TYPE = "AMRAP"
NOW = datetime.datetime.utcnow()


def test_wod_type(db):
    new_type = wod.WodType(name=WOD_TYPE)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    assert new_type.id == 1
    assert new_type.name == WOD_TYPE

    new_type = wod.WodType()
    db.add(new_type)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()

    assert (
        'null value in column "name" of relation "wod_board_wod_type" violates'
        " not-null constraint" in str(error)
    )


def test_wod(db):
    new_type = wod.WodType(name=WOD_TYPE)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    new_wod = wod.Wod(date=NOW, wod_type_id=new_type.id)
    db.add(new_wod)
    db.commit()

    db.refresh(new_wod)

    assert new_wod.id == 1
    assert new_wod.description is None
    assert new_wod.note is None
    assert new_wod.date == NOW
    assert new_wod.wod_type_id == new_type.id

    new_wod = wod.Wod(date=NOW)
    db.add(new_wod)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()

    assert (
        'null value in column "wod_type_id" of relation "wod_board_wod" violates'
        " not-null constraint" in str(error)
    )
