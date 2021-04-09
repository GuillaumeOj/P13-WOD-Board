import datetime

import pytest
import sqlalchemy.exc

from wod_board.models import wod


WOD_TYPE = "AMRAP"
NOW = datetime.datetime.utcnow()


def test_wod_type(db):
    new_type = wod.WodType(WOD_TYPE)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    assert new_type.id == 1
    assert new_type.name == WOD_TYPE


def test_wod(db):
    new_type = wod.WodType(WOD_TYPE)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    new_wod = wod.Wod(
        new_type.id,
        date=NOW,
    )
    db.add(new_wod)
    db.commit()

    db.refresh(new_wod)

    assert new_wod.id == 1
    assert new_wod.description is None
    assert new_wod.note is None
    assert new_wod.date == NOW
    assert new_wod.wod_type_id == new_type.id


def test_round(db):
    wod_type = wod.WodType(WOD_TYPE)
    new_wod = wod.Wod(1)
    db.add(wod_type)
    db.add(new_wod)
    db.commit()

    first_round = wod.Round(position=1, wod_id=new_wod.id)
    db.add(first_round)
    db.commit()
    db.refresh(first_round)

    assert first_round.id == 1
    assert first_round.position == 1
    assert first_round.duration_seconds is None
    assert first_round.wod_id == new_wod.id
    assert first_round.parent_id is None

    second_round = wod.Round(
        position=2,
        duration_seconds=20,
        wod_id=new_wod.id,
    )
    db.add(second_round)
    db.commit()
    db.refresh(second_round)

    assert second_round.id == 2
    assert second_round.position == 2
    assert second_round.duration_seconds == 20
    assert second_round.wod_id == new_wod.id
    assert second_round.parent_id is None

    third_round = wod.Round(
        position=3,
        duration_seconds=20,
        wod_id=new_wod.id,
        parent_id=first_round.id,
    )
    db.add(third_round)
    db.commit()
    db.refresh(third_round)

    assert third_round.id == 3
    assert third_round.position == 3
    assert third_round.duration_seconds == 20
    assert third_round.wod_id == new_wod.id
    assert third_round.parent_id == first_round.id


def test_round_unique_constraint(db):
    wod_type = wod.WodType(WOD_TYPE)
    new_wod = wod.Wod(1)
    db.add(wod_type)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    first_round = wod.Round(position=1, wod_id=new_wod.id)
    second_round = wod.Round(position=1, wod_id=new_wod.id)
    db.add(first_round)
    db.add(second_round)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()

    assert 'duplicate key value violates unique constraint "wod_id_position"' in str(
        error
    )
