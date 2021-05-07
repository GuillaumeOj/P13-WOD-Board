import pytest
import sqlalchemy.exc

from wod_board.models import w_type


def test_type(db):
    wod_type = w_type.WodType(name="AMRAP")
    db.add(wod_type)
    db.commit()
    db.refresh(wod_type)

    assert wod_type.id == 1
    assert wod_type.name == "AMRAP"

    wod_type = w_type.WodType(name="AMRAP")
    db.add(wod_type)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()

    assert 'duplicate key value violates unique constraint "wod_type_name_key"' in str(
        error
    )
