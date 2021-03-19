import pytest
import sqlalchemy.exc

from wod_board.models import wod
from wod_board.models import wod_round


def test_round(db):
    wod_type = wod.WodType(name="AMRAP")
    new_wod = wod.Wod(wod_type_id=1)
    db.add(wod_type)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    first_round = wod_round.Round(position=1, wod_id=new_wod.id)
    db.add(first_round)
    db.commit()
    db.refresh(first_round)

    assert first_round.id == 1
    assert first_round.position == 1
    assert first_round.duration_seconds is None
    assert first_round.parent_id is None
    assert first_round.wod_id == new_wod.id

    first_sub_round = wod_round.Round(
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

    second_sub_round = wod_round.Round(
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

    first_round = wod_round.Round(position=1, wod_id=new_wod.id)
    second_round = wod_round.Round(position=1, wod_id=new_wod.id)
    db.add(first_round)
    db.add(second_round)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()

    assert 'duplicate key value violates unique constraint "wod_id_position"' in str(
        error
    )
