import datetime

import pytest
import sqlalchemy.exc

from wod_board.models import movement
from wod_board.models import wod
from wod_board.models import wod_round


WOD_TYPE = "AMRAP"
NOW = datetime.datetime.utcnow()


def test_round(db):
    wod_type = wod.WodType(name=WOD_TYPE)
    new_wod = wod.Wod(wod_type=wod_type)

    sub_round = wod_round.Round(position=3, wod=new_wod)
    first_round = wod_round.Round(position=1, wod=new_wod, sub_rounds=[sub_round])
    db.add(first_round)
    db.commit()
    db.refresh(first_round)

    assert first_round.position == 1
    assert first_round.wod_id == new_wod.id
    assert first_round.sub_rounds.count() == 1


def test_round_unique_constraint(db):
    wod_type = wod.WodType(name=WOD_TYPE)
    new_wod = wod.Wod(wod_type=wod_type)

    first_round = wod_round.Round(position=1, wod=new_wod)
    second_round = wod_round.Round(position=1, wod=new_wod)
    db.add(first_round)
    db.add(second_round)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()

    db.rollback()

    assert 'duplicate key value violates unique constraint "wod_id_position"' in str(
        error
    )
    assert db.query(wod_round.Round).count() == 0


def test_round_with_movement(db):
    devil_press = movement.Movement(name="Devil Press")
    devil_press_goal = movement.MovementGoal(movement=devil_press)

    wod_type = wod.WodType(name=WOD_TYPE)
    new_wod = wod.Wod(wod_type=wod_type)

    first_round = wod_round.Round(wod=new_wod, position=1, movements=[devil_press_goal])

    db.add(first_round)
    db.commit()

    rounds = db.query(wod_round.Round)

    assert rounds.count() == 1
    assert rounds.first().position == first_round.position
    assert rounds.first().movements.count() == 1
