import typing

import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import unit
from wod_board.schemas import unit_schemas


def _create_unit(
    db: sqlalchemy.orm.Session,
    unit_schema: unit_schemas.UnitCreate,
) -> unit.Unit:
    new_unit = unit.Unit(**unit_schema.dict())
    db.add(new_unit)

    db.commit()
    db.refresh(new_unit)

    return new_unit


def get_unit_by_exact_name(
    db: sqlalchemy.orm.Session,
    name: str,
) -> unit.Unit:
    db_unit: typing.Optional[unit.Unit] = (
        db.query(unit.Unit).filter(unit.Unit.name == name).first()
    )

    if db_unit is None:
        raise exceptions.UnknownUnit

    return db_unit


def get_or_create_unit(
    db: sqlalchemy.orm.Session,
    wanted_unit: unit_schemas.UnitCreate,
) -> unit.Unit:
    try:
        db_unit = get_unit_by_exact_name(db, wanted_unit.name)
    except exceptions.UnknownUnit:
        db_unit = _create_unit(db, wanted_unit)

    return db_unit
