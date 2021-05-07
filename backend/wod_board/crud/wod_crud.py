import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import wod
from wod_board.schemas import wod_schemas


LOG = daiquiri.getLogger(__name__)


def create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod.WodType:
    new_type = wod.WodType(name=wod_type.name)
    db.add(new_type)

    db.commit()
    db.refresh(new_type)

    return new_type


def get_wod_type_by_name(db: sqlalchemy.orm.Session, name: str) -> wod.WodType:
    db_wod_type: typing.Optional[wod.WodType] = (
        db.query(wod.WodType).filter(wod.WodType.name == name).first()
    )

    if db_wod_type is None:
        raise exceptions.UnknownWodType

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
    except exceptions.UnknownWodType:
        db_wod_type = create_wod_type(db, wod_type)

    return db_wod_type


def get_wod_by_id(db: sqlalchemy.orm.Session, id: int) -> wod.Wod:
    db_wod: wod.Wod = db.get(wod.Wod, id)

    if db_wod is None:
        raise exceptions.UnknownWod

    return db_wod


def create_wod(
    db: sqlalchemy.orm.Session,
    wod_data: wod_schemas.WodCreate,
) -> wod.Wod:
    new_wod = wod.Wod(**wod_data.dict())

    db.add(new_wod)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'insert or update on table "wod" violates foreign '
            'key constraint "wod_wod_type_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownWodType
        if (
            'insert or update on table "wod" violates foreign '
            'key constraint "wod_author_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownUser
        if ('duplicate key value violates unique constraint "wod_title_key"') in str(
            error
        ):
            raise exceptions.TitleAlreadyUsed
        LOG.error(error)
    db.refresh(new_wod)

    return new_wod


def update_wod(
    db: sqlalchemy.orm.Session,
    wod_data: wod_schemas.WodCreate,
    wod_id: int,
) -> wod.Wod:
    db_wod: typing.Optional[wod.Wod] = db.get(wod.Wod, wod_id)

    if db_wod is None:
        raise exceptions.UnknownWod

    db_wod.title = wod_data.title
    db_wod.description = wod_data.description
    db_wod.date = wod_data.date
    db_wod.author_id = wod_data.author_id
    db_wod.wod_type_id = wod_data.wod_type_id

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'insert or update on table "wod" violates foreign '
            'key constraint "wod_wod_type_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownWodType
        if (
            'insert or update on table "wod" violates foreign '
            'key constraint "wod_author_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownUser
        if ('duplicate key value violates unique constraint "wod_title_key"') in str(
            error
        ):
            raise exceptions.TitleAlreadyUsed
        LOG.error(error)

    db.refresh(db_wod)

    return db_wod


def get_wod_by_id(db: sqlalchemy.orm.Session, wod_id: int) -> wod.Wod:
    db_wod: typing.Optional[wod.Wod] = db.get(wod.Wod, wod_id)

    if db_wod is None:
        raise exceptions.UnknownWod

    return db_wod
