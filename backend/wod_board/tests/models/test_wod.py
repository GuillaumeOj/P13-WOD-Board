import datetime

from wod_board.models import wod


NOW = datetime.datetime.utcnow()


def test_wod_type(db):
    wod_type = wod.WodType(name="AMRAP")
    db.add(wod_type)
    db.commit()
    db.refresh(wod_type)

    assert wod_type.id == 1
    assert wod_type.name == "AMRAP"


def test_wod(db):
    new_wod = wod.Wod(date=NOW)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    assert new_wod.id == 1
    assert new_wod.description is None
    assert new_wod.note is None
    assert new_wod.date == NOW
