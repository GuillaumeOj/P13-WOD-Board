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
        'null value in column "name" of relation "wod_type" violates'
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
        'null value in column "wod_type_id" of relation "wod" violates'
        " not-null constraint" in str(error)
    )


def test_wod_with_rounds(db):
    new_type = wod.WodType(name=WOD_TYPE)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    new_wod = wod.Wod(date=NOW, wod_type_id=new_type.id)
    db.add(new_wod)
    db.commit()

    db.refresh(new_wod)

    first_round = wod.Round(position=1, wod_id=new_wod.id)
    db.add(first_round)
    db.commit()
    db.refresh(first_round)
    db.refresh(new_wod)

    assert len(new_wod.rounds) == 1
    assert first_round in new_wod.rounds


def test_round(db):
    wod_type = wod.WodType(name="AMRAP")
    new_wod = wod.Wod(wod_type_id=1)
    db.add(wod_type)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    first_round = wod.Round(position=1, wod_id=new_wod.id)
    db.add(first_round)
    db.commit()
    db.refresh(first_round)

    assert first_round.id == 1
    assert first_round.position == 1
    assert first_round.duration_seconds is None
    assert first_round.parent_id is None
    assert first_round.wod_id == new_wod.id

    first_sub_round = wod.Round(
        position=2,
        parent_id=first_round.id,
        duration_seconds=20,
        wod_id=first_round.wod_id,
    )
    db.add(first_sub_round)
    db.commit()
    db.refresh(first_sub_round)

    assert first_sub_round.id == 2
    assert first_sub_round.position == 2
    assert first_sub_round.duration_seconds == 20
    assert first_sub_round.parent_id == first_round.id
    assert first_sub_round.wod_id == new_wod.id

    second_sub_round = wod.Round(
        position=3,
        parent_id=first_round.id,
        duration_seconds=10,
        wod_id=first_round.wod_id,
    )
    db.add(second_sub_round)
    db.commit()
    db.refresh(second_sub_round)

    assert second_sub_round.id == 3
    assert second_sub_round.position == 3
    assert second_sub_round.duration_seconds == 10
    assert second_sub_round.parent_id == first_round.id
    assert second_sub_round.wod_id == new_wod.id


def test_round_unique_constraint(db):
    wod_type = wod.WodType(name="AMRAP")
    new_wod = wod.Wod(wod_type_id=1)
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
