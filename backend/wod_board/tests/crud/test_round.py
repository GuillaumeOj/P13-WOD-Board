import pytest

from wod_board import exceptions
from wod_board.crud import round_crud
from wod_board.models import wod_round
from wod_board.schemas import round_schemas


def test_create_round(db, db_wod, db_user):
    assert db.query(wod_round.Round).count() == 0

    wanted_round = round_schemas.RoundCreate(
        position=1,
        duration_seconds=60,
        repetition=5,
        wod_id=db_wod.id,
    )
    round_crud.create_round(db, wanted_round, db_user.id)
    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(exceptions.DuplicatedRoundPosition):
        round_crud.create_round(db, wanted_round, db_user.id)
    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(exceptions.UserIsNotAuthor):
        round_crud.create_round(db, wanted_round, 2)
    assert db.query(wod_round.Round).count() == 1

    wanted_round = round_schemas.RoundCreate(
        position=1,
        duration_seconds=60,
        repetition=5,
        wod_id=2,
    )
    with pytest.raises(exceptions.UnknownWod):
        round_crud.create_round(db, wanted_round, db_user.id)
    assert db.query(wod_round.Round).count() == 1


def test_update_round(db, db_round, db_user):
    assert db.query(wod_round.Round).count() == 1

    round_schema = round_schemas.RoundCreate(
        position=db_round.position,
        duration_seconds=60,
        repetition=5,
        wod_id=db_round.wod_id,
    )
    assert db_round.duration_seconds != round_schema.duration_seconds
    assert db_round.repetition != round_schema.repetition

    round_crud.update_round(db, round_schema, db_round.id, db_user.id)
    db_round = db.get(wod_round.Round, db_round.id)
    assert db_round.duration_seconds == round_schema.duration_seconds
    assert db_round.repetition == round_schema.repetition
    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(exceptions.UnknownRound):
        round_crud.update_round(db, round_schema, 2, db_user.id)
    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(exceptions.UserIsNotAuthor):
        round_crud.update_round(db, round_schema, db_round.id, 2)
    assert db.query(wod_round.Round).count() == 1

    round_schema = round_schemas.RoundCreate(
        position=db_round.position,
        duration_seconds=60,
        repetition=5,
        wod_id=2,
    )
    with pytest.raises(exceptions.UnknownWod):
        round_crud.update_round(db, round_schema, db_round.id, db_user.id)
    assert db.query(wod_round.Round).count() == 1

    db.add(
        wod_round.Round(
            position=2, repetition=0, duration_seconds=0, wod_id=db_round.wod_id
        )
    )
    db.commit()
    assert db.query(wod_round.Round).count() == 2

    round_schema = round_schemas.RoundCreate(
        position=2,
        duration_seconds=60,
        repetition=5,
        wod_id=db_round.wod_id,
    )
    with pytest.raises(exceptions.DuplicatedRoundPosition):
        round_crud.update_round(db, round_schema, db_round.id, db_user.id)
    assert db.query(wod_round.Round).count() == 2


def test_delete_round_by_id(db, db_round, db_user):
    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(exceptions.UnknownRound):
        round_crud.delete_round_by_id(db, 2, db_user.id)
    assert db.query(wod_round.Round).count() == 1

    with pytest.raises(exceptions.UserIsNotAuthor):
        round_crud.delete_round_by_id(db, db_round.id, 2)
    assert db.query(wod_round.Round).count() == 1

    assert round_crud.delete_round_by_id(db, db_round.id, db_user.id)
    assert db.query(wod_round.Round).count() == 0


def test_get_rounds_by_wod_id(db, db_round):
    assert db.query(wod_round.Round).count() == 1

    rounds = round_crud.get_rounds_by_wod_id(db, db_round.id)
    assert len(rounds) == 1
    assert db.query(wod_round.Round).count() == 1

    rounds = round_crud.get_rounds_by_wod_id(db, 2)
    assert len(rounds) == 0
    assert db.query(wod_round.Round).count() == 1
