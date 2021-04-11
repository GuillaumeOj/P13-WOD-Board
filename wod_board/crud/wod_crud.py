import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.models import wod
from wod_board.schemas import wod_schemas


class UnknownWodType(Exception):
    pass


class DuplicatedRoundPosition(Exception):
    pass


class WrongWodId(Exception):
    pass


def _create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod.WodType:
    new_type = wod.WodType(name=wod_type.name)
    db.add(new_type)

    db.commit()
    db.refresh(new_type)

    return new_type


def _get_wod_type_by_exact_name(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod.WodType:
    db_wod_type: wod.WodType = (
        db.query(wod.WodType).filter(wod.WodType.name == wod_type.name).first()
    )

    if db_wod_type is None:
        raise UnknownWodType

    return db_wod_type


def get_or_create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod.WodType:
    try:
        db_wod_type = _get_wod_type_by_exact_name(db, wod_type)
    except UnknownWodType:
        db_wod_type = _create_wod_type(db, wod_type)

    return db_wod_type


def create_wod(
    db: sqlalchemy.orm.Session,
    wod_data: wod_schemas.WodCreate,
) -> wod.Wod:

    wod_type = wod_schemas.WodType.from_orm(
        get_or_create_wod_type(db, wod_data.wod_type)
    )

    new_wod = wod.Wod(
        wod_type_id=wod_type.id,
        description=wod_data.description,
        note=wod_data.note,
        date=wod_data.date,
    )

    db.add(new_wod)

    db.commit()
    db.refresh(new_wod)

    return new_wod
