import typing

import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board import models
from wod_board.models import equipment
from wod_board.models import movement
from wod_board.models import unit
from wod_board.models import user


def users(db: sqlalchemy.orm.Session) -> None:
    admin_password = "very-strong-password"
    hashed_admin_password = config.PASSWORD_CTXT.hash(admin_password)
    db.add(
        user.User(
            email="admin@bar.com",
            username="admin-bar",
            password=hashed_admin_password,
            is_admin=True,
        )
    )

    user_password = "very-strong-password"
    hashed_user_password = config.PASSWORD_CTXT.hash(user_password)
    db.add(
        user.User(
            email="foo@bar.com",
            username="foo-bar",
            password=hashed_user_password,
            is_admin=False,
        )
    )

    db.commit()


def units(db: sqlalchemy.orm.Session) -> None:
    db.add(unit.Unit(name="Unit", symbol="U"))
    db.add(unit.Unit(name="Kilogram", symbol="kg"))
    db.add(unit.Unit(name="Meter", symbol="m"))

    db.commit()


def equipments(db: sqlalchemy.orm.Session) -> None:
    kilogram: typing.Optional[unit.Unit] = (
        db.query(unit.Unit).filter(unit.Unit.name == "Kilogram").first()
    )

    if kilogram is None:
        raise exceptions.UnknownUnit

    db.add(equipment.Equipment(name="Dumbbell", unit_id=kilogram.id))
    db.add(equipment.Equipment(name="Kettlebell", unit_id=kilogram.id))
    db.add(equipment.Equipment(name="Barbell", unit_id=kilogram.id))

    db.commit()


def movements(db: sqlalchemy.orm.Session) -> None:
    unit_u: typing.Optional[unit.Unit] = (
        db.query(unit.Unit).filter(unit.Unit.name == "Unit").first()
    )
    meter: typing.Optional[unit.Unit] = (
        db.query(unit.Unit).filter(unit.Unit.name == "Meter").first()
    )

    if unit_u is None or meter is None:
        raise exceptions.UnknownUnit

    dumbbell = (
        db.query(equipment.Equipment)
        .filter(equipment.Equipment.name == "Dumbbell")
        .first()
    )
    kettlebell = (
        db.query(equipment.Equipment)
        .filter(equipment.Equipment.name == "Kettlebell")
        .first()
    )
    barebell = (
        db.query(equipment.Equipment)
        .filter(equipment.Equipment.name == "Barbell")
        .first()
    )

    db.add(
        movement.Movement(
            name="Devil Press",
            unit_id=unit_u.id,
            equipments=[dumbbell, kettlebell],
        )
    )

    db.add(
        movement.Movement(
            name="Dead Lift",
            unit_id=unit_u.id,
            equipments=[barebell],
        )
    )
    db.add(movement.Movement(name="Burpees", unit_id=unit_u.id))
    db.add(movement.Movement(name="Run", unit_id=meter.id))

    db.commit()


def seed_db() -> None:
    models.drop_all()
    models.create_all()

    db = models.Session()

    if config.WOD_BOARD_ENV == "production":
        return

    users(db)
    units(db)
    equipments(db)
    movements(db)


if __name__ == "__main__":
    seed_db()
