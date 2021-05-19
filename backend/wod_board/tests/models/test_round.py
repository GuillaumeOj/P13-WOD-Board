import datetime

import pytest
import sqlalchemy.exc

from wod_board.models import wod_round


WOD_TYPE = "AMRAP"
NOW = datetime.datetime.utcnow()


def test_round(db, db_wod):
    sub_round = wod_round.Round(
        position=2,
        repetition=0,
        duration_seconds=0,
        wod_id=db_wod.id,
    )
    first_round = wod_round.Round(
        position=1,
        repetition=0,
        duration_seconds=0,
        wod_id=db_wod.id,
        sub_rounds=[sub_round],
    )
    db.add(first_round)
    db.commit()
    db.refresh(first_round)

    assert first_round.position == 1
    assert first_round.sub_rounds.count() == 1

    third_round = wod_round.Round(
        position=1,
        repetition=0,
        duration_seconds=0,
        wod_id=db_wod.id,
    )
    db.add(third_round)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()

    db.rollback()

    assert 'duplicate key value violates unique constraint "wod_id_position"' in str(
        error
    )
    assert db.query(wod_round.Round).count() == 2

    db.delete(db_wod)
    db.commit()
    assert db.query(wod_round.Round).count() == 0
