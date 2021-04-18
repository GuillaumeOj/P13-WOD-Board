from wod_board.models import equipment


def test_equipment(db):
    dumbbell = equipment.Equipment(name="Dumbbell")

    db.add(dumbbell)
    db.commit()

    equipments = db.query(equipment.Equipment)

    assert equipments.count() == 1
    assert equipments.first().name == dumbbell.name
