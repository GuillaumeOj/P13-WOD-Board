import pytest

from wod_board.crud import round_crud
from wod_board.models import wod
from wod_board.models import wod_round
from wod_board.schemas import round_schemas


def test_create_round(db):
    wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    sub_round = round_schemas.RoundCreate(position=2, wod_id=db_wod.id)
    first_round = round_schemas.RoundCreate(
        position=1,
        duration_seconds=60,
        repetition=5,
        wod_id=db_wod.id,
        sub_rounds=[sub_round],
    )

    round_crud.create_round(db, first_round)
    assert db.query(wod_round.Round).count() == 2

    parent_round = (
        db.query(wod_round.Round).filter(wod_round.Round.position == 1).first()
    )
    assert parent_round.sub_rounds.count() == 1


def test_update_round(db):
    db_wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=db_wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    db_round = wod_round.Round(position=1, wod_id=db_wod.id)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    round_schema = round_schemas.RoundCreate(
        position=db_round.position,
        duration_seconds=60,
        repetition=5,
        wod_id=db_round.wod_id,
    )

    assert db_round.duration_seconds != round_schema.duration_seconds
    assert db_round.repetition != round_schema.repetition

    round_crud.update_round(db, round_schema, db_round.id)
    db_round = db.get(wod_round.Round, db_round.id)
    assert db_round.duration_seconds == round_schema.duration_seconds
    assert db_round.repetition == round_schema.repetition

    with pytest.raises(round_crud.UnknownRound):
        round_crud.update_round(db, round_schema, 2)


def test_create_rounds_with_duplicated_position(db):
    wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    first_round = round_schemas.RoundCreate(position=1, wod_id=db_wod.id)
    first_sub_round = round_schemas.RoundCreate(position=1, wod_id=db_wod.id)
    first_round.sub_rounds = [first_sub_round]

    with pytest.raises(round_crud.DuplicatedRoundPosition):
        round_crud.create_round(db, first_round)


def test_delete_round_by_id(db):
    wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    db_round = wod_round.Round(wod_id=db_wod.id, position=1)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(round_crud.UnknownRound):
        round_crud.delete_round_by_id(db, 2)

    assert db.query(wod_round.Round).count() == 1

    assert round_crud.delete_round_by_id(db, db_round.id)
    assert db.query(wod_round.Round).count() == 0
