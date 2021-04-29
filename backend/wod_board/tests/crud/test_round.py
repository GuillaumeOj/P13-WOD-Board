import pytest

from wod_board.crud import round_crud
from wod_board.models import wod_round
from wod_board.schemas import round_schemas


def test_create_round(db, db_wod):
    assert db.query(wod_round.Round).count() == 0

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

    with pytest.raises(round_crud.DuplicatedRoundPosition):
        round_crud.create_round(db, first_round)
    assert db.query(wod_round.Round).count() == 2


def test_update_round(db, db_round):
    assert db.query(wod_round.Round).count() == 1

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
    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(round_crud.UnknownRound):
        round_crud.update_round(db, round_schema, 2)
    assert db.query(wod_round.Round).count() == 1


def test_delete_round_by_id(db, db_round):
    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(round_crud.UnknownRound):
        round_crud.delete_round_by_id(db, 2)

    assert db.query(wod_round.Round).count() == 1

    assert round_crud.delete_round_by_id(db, db_round.id)
    assert db.query(wod_round.Round).count() == 0
