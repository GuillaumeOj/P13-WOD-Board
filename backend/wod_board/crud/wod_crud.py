import typing

import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.models import wod
from wod_board.schemas import wod_schemas


class UnknownWodType(Exception):
    pass


class UnknownWod(Exception):
    pass


class WrongWodId(Exception):
    pass


def create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod.WodType:
    new_type = wod.WodType(name=wod_type.name)
    db.add(new_type)

    db.commit()
    db.refresh(new_type)

    return new_type


def get_wod_type_by_name(db: sqlalchemy.orm.Session, name: str) -> wod.WodType:
    db_wod_type: wod.WodType = (
        db.query(wod.WodType).filter(wod.WodType.name == name).first()
    )

    if db_wod_type is None:
        raise UnknownWodType

    return db_wod_type


def get_wod_types_by_name(
    db: sqlalchemy.orm.Session, name: str
) -> typing.List[typing.Optional[wod.WodType]]:
    db_wod_types: typing.List[typing.Optional[wod.WodType]] = (
        db.query(wod.WodType).filter(wod.WodType.name.ilike(f"%{name}%")).all()
    )

    return db_wod_types


def get_wod_type_all(
    db: sqlalchemy.orm.Session,
) -> typing.List[typing.Optional[wod.WodType]]:
    db_wod_types: typing.List[typing.Optional[wod.WodType]] = (
        db.query(wod.WodType).order_by(wod.WodType.name).all()
    )

    return db_wod_types


def get_or_create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod.WodType:
    try:
        db_wod_type = get_wod_type_by_name(db, wod_type.name)
    except UnknownWodType:
        db_wod_type = create_wod_type(db, wod_type)

    return db_wod_type


def get_wod_by_id(db: sqlalchemy.orm.Session, id: int) -> wod.Wod:
    db_wod: wod.Wod = db.get(wod.Wod, id)

    if db_wod is None:
        raise UnknownWod

    return db_wod


def create_wod(
    db: sqlalchemy.orm.Session,
    wod_data: wod_schemas.WodCreate,
) -> wod.Wod:

    wod_type = get_or_create_wod_type(db, wod_data.wod_type)

    new_wod = wod.Wod(
        description=wod_data.description,
        note=wod_data.note,
        date=wod_data.date,
        wod_type=wod_type,
    )

    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    return new_wod


def update_wod(
    db: sqlalchemy.orm.Session,
    wod_data: wod_schemas.WodCreate,
    wod_id: int,
) -> wod.Wod:

    wod_to_update: wod.Wod = db.get(wod.Wod, wod_id)

    if wod_to_update is None:
        raise UnknownWod

    wod_type = get_or_create_wod_type(db, wod_data.wod_type)

    wod_to_update.description = wod_data.description
    wod_to_update.note = wod_data.note
    wod_to_update.date = wod_data.date
    wod_to_update.wod_type = wod_type

    db.commit()
    db.refresh(wod_to_update)

    return wod_to_update
