from wod_board import models
from wod_board import seed


def test_seed(db):
    seed.seed_db()

    assert db.query(models.User).count() > 0
    assert db.query(models.Unit).count() > 0
    assert db.query(models.Equipment).count() > 0
    assert db.query(models.Movement).count() > 0

    assert db.query(models.User).filter(models.User.username == "admin-bar").first()
