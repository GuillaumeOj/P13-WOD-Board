from wod_board import seed
from wod_board.models import equipment
from wod_board.models import movement
from wod_board.models import unit
from wod_board.models import user


def test_seed(db):
    seed.seed_db()

    assert db.query(user.User).count() > 0
    assert db.query(unit.Unit).count() > 0
    assert db.query(equipment.Equipment).count() > 0
    assert db.query(movement.Movement).count() > 0

    assert db.query(user.User).filter(user.User.username == "admin-bar").first()
