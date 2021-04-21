import pytest

from wod_board.crud import round_crud
from wod_board.models import movement
from wod_board.models import wod
from wod_board.models import wod_round
from wod_board.schemas import movement_schemas
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


def test_create_round_with_mouvement(db):
    wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    devil_press = movement_schemas.MovementCreate(name="Devil Press")
    db.add(movement.Movement(name=devil_press.name))
    db.commit()

    goal = movement_schemas.MovementGoalCreate(movement=devil_press)

    first_round = round_schemas.RoundCreate(
        position=1, wod_id=db_wod.id, movements=[goal]
    )

    round_crud.create_round(db, first_round)
    assert db.query(movement.MovementGoal).count() == 1


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
