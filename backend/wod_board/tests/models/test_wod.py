import datetime

import pytest
import sqlalchemy.exc

from wod_board.models import wod


NOW = datetime.datetime.utcnow()


def test_wod(db, db_user):
    assert db.query(wod.Wod).count() == 0

    new_wod = wod.Wod(title="Murph", is_complete=True, author_id=db_user.id, date=NOW)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)
    assert db.query(wod.Wod).count() == 1
    assert new_wod.title == "Murph"
    assert new_wod.description is None
    assert new_wod.date == NOW
    assert new_wod.author_id == db_user.id

    same_wod = wod.Wod(title="Murph", is_complete=True, author_id=db_user.id, date=NOW)
    db.add(same_wod)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()
    db.rollback()
    assert 'duplicate key value violates unique constraint "wod_title_key"' in str(
        error
    )
    assert db.query(wod.Wod).count() == 1

    new_wod = wod.Wod(title="Karen", is_complete=True, author_id=2, date=NOW)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.add(new_wod)
        db.commit()
    db.rollback()
    assert (
        'insert or update on table "wod" violates foreign key '
        'constraint "wod_author_id_fkey"' in str(error)
    )
    assert db.query(wod.Wod).count() == 1

    db.delete(db_user)
    db.commit()
    assert db.query(wod.Wod).count() == 0
