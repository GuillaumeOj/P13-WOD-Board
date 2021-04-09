import sqlalchemy.orm

from wod_board.models import unit
from wod_board.schemas import unit_schemas


class UnknownUnit(Exception):
    pass


def _create_unit(
    db: sqlalchemy.orm.Session,
    unit_schema: unit_schemas.UnitCreate,
) -> unit.Unit:
    new_unit = unit.Unit(**unit_schema.dict())
    db.add(new_unit)

    db.commit()
    db.refresh(new_unit)

    return new_unit


def _get_unit_by_exact_name(
    db: sqlalchemy.orm.Session,
    wanted_unit: unit_schemas.UnitCreate,
) -> unit.Unit:
    db_unit: unit.Unit = (
        db.query(unit.Unit).filter(unit.Unit.name == wanted_unit.name).first()
    )

    if db_unit is None:
        raise UnknownUnit

    return db_unit


def get_or_create_unit(
    db: sqlalchemy.orm.Session,
    wanted_unit: unit_schemas.UnitCreate,
) -> unit_schemas.Unit:
    try:
        db_unit = _get_unit_by_exact_name(db, wanted_unit)
    except UnknownUnit:
        db_unit = _create_unit(db, wanted_unit)

    return unit_schemas.Unit.from_orm(db_unit)
