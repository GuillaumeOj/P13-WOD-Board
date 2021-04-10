import datetime

from wod_board.models import wod


WOD_TYPE = "AMRAP"
NOW = datetime.datetime.utcnow()


def test_wod_type(db):
    new_type = wod.WodType(WOD_TYPE)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    assert new_type.id == 1
    assert new_type.name == WOD_TYPE


def test_wod(db):
    new_type = wod.WodType(WOD_TYPE)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    new_wod = wod.Wod(
        new_type.id,
        date=NOW,
    )
    db.add(new_wod)
    db.commit()

    db.refresh(new_wod)

    assert new_wod.id == 1
    assert new_wod.description is None
    assert new_wod.note is None
    assert new_wod.date == NOW
    assert new_wod.wod_type_id == new_type.id
