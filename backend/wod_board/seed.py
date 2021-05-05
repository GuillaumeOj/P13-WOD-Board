from wod_board import config
from wod_board import models


def users(db):
    admin_password = "very-strong-password"
    hashed_admin_password = config.PASSWORD_CTXT.hash(admin_password)
    db.add(
        models.User(
            email="admin@bar.com",
            username="admin-bar",
            hashed_password=hashed_admin_password,
            is_admin=True,
        )
    )

    user_password = "very-strong-password"
    hashed_user_password = config.PASSWORD_CTXT.hash(user_password)
    db.add(
        models.User(
            email="foo@bar.com",
            username="foo-bar",
            hashed_password=hashed_user_password,
            is_admin=False,
        )
    )

    db.commit()


def units(db):
    db.add(models.Unit(name="Unit", symbol="U"))
    db.add(models.Unit(name="Kilogram", symbol="kg"))
    db.add(models.Unit(name="Meter", symbol="m"))

    db.commit()


def equipments(db):
    kilogram = db.query(models.Unit).filter(models.Unit.name == "Kilogram").first()

    db.add(models.Equipment(name="Dumbbell", unit_id=kilogram.id))
    db.add(models.Equipment(name="Kettlebell", unit_id=kilogram.id))
    db.add(models.Equipment(name="Barbell", unit_id=kilogram.id))

    db.commit()


def movements(db):
    unit = db.query(models.Unit).filter(models.Unit.name == "Unit").first()
    meter = db.query(models.Unit).filter(models.Unit.name == "Meter").first()

    dumbbell = (
        db.query(models.Equipment).filter(models.Equipment.name == "Dumbbell").first()
    )
    kettlebell = (
        db.query(models.Equipment).filter(models.Equipment.name == "Kettlebell").first()
    )
    barebell = (
        db.query(models.Equipment).filter(models.Equipment.name == "Barbell").first()
    )

    db.add(
        models.Movement(
            name="Devil Press",
            unit_id=unit.id,
            equipments=[dumbbell, kettlebell],
        )
    )

    db.add(
        models.Movement(
            name="Dead Lift",
            unit_id=unit.id,
            equipments=[barebell],
        )
    )
    db.add(models.Movement(name="Burpees", unit_id=unit.id))
    db.add(models.Movement(name="Run", unit_id=meter.id))

    db.commit()


def seed_db():
    models.drop_all()
    models.create_all()

    db = models.Session()

    users(db)
    units(db)
    equipments(db)
    movements(db)


if __name__ == "__main__":
    seed_db()
