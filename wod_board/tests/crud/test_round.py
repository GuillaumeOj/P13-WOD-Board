import pytest

from wod_board.crud import round_crud
from wod_board.models import wod
from wod_board.models import wod_round
from wod_board.schemas import round_schemas


def test_create_round(db):
    wod_type = wod.WodType("AMRAP")
    new_wod = wod.Wod(wod_type_id=1)
    db.add(wod_type)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    first_round = round_schemas.RoundCreate(position=1, wod_id=new_wod.id)
    first_sub_round = round_schemas.RoundCreate(position=2, wod_id=new_wod.id)
    first_round.children = [first_sub_round]

    round_crud.create_round(db, first_round)

    db_rounds = db.query(wod_round.Round).all()
    assert len(db_rounds) == 2

    parent_round = (
        db.query(wod_round.Round).filter(wod_round.Round.position == 1).first()
    )
    assert parent_round.children.count() == 1


def test_create_rounds_with_duplicated_position(db):
    wod_type = wod.WodType("AMRAP")
    new_wod = wod.Wod(wod_type_id=1)
    db.add(wod_type)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    first_round = round_schemas.RoundCreate(position=1, wod_id=new_wod.id)
    first_sub_round = round_schemas.RoundCreate(position=1, wod_id=new_wod.id)
    first_round.children = [first_sub_round]

    with pytest.raises(round_crud.DuplicatedRoundPosition):
        round_crud.create_round(db, first_round)
