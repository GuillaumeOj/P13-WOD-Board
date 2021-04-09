from wod_board.models import equipment
from wod_board.models import movement
from wod_board.models import unit


def test_movement(db):
    dumbbell = equipment.Equipment(name="Dumbbell")
    simple_unit = unit.Unit(name="unit", symbol="u")
    db.add(simple_unit)
    db.commit()
    db.refresh(simple_unit)

    devil_press = movement.Movement(name="Devil Press", unit_id=simple_unit.id)
    devil_press.equipments.append(dumbbell)

    db.add(devil_press)
    db.commit()

    movements = db.query(movement.Movement)

    assert movements.count() == 1
    assert movements.first().name == devil_press.name
    assert movements.first().unit_id == simple_unit.id
    assert movements.first().equipments.count() == 1
