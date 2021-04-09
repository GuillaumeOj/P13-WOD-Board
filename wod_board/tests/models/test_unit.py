import pytest
import sqlalchemy.exc

from wod_board.models import unit


def test_unit(db):
    kilograms = unit.Unit(name="Kilograms", symbol="kg")

    db.add(kilograms)
    db.commit()

    units = db.query(unit.Unit)

    assert units.count() == 1
    assert units.first().name == kilograms.name
    assert units.first().symbol == kilograms.symbol

    kilograms2 = unit.Unit(name="Kilograms", symbol="kg")
    db.add(kilograms2)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()

    assert 'duplicate key value violates unique constraint "name_symbol"' in str(error)
