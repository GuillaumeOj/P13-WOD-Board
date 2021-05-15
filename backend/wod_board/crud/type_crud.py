import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import w_type
from wod_board.schemas import type_schemas


LOG = daiquiri.getLogger(__name__)


def create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: type_schemas.WodTypeCreate
) -> w_type.WodType:
    new_type = w_type.WodType(**wod_type.dict())
    db.add(new_type)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if 'duplicate key value violates unique constraint "wod_type_name_key"' in str(
            error
        ):
            raise exceptions.NameAlreadyUsed(wod_type.name)
        LOG.error(str(error))

    db.refresh(new_type)

    return new_type


def get_wod_type_by_name(db: sqlalchemy.orm.Session, name: str) -> w_type.WodType:
    db_wod_type: typing.Optional[w_type.WodType] = (
        db.query(w_type.WodType).filter(w_type.WodType.name == name).first()
    )

    if db_wod_type is None:
        raise exceptions.UnknownWodType(name)

    return db_wod_type


def get_wod_types_by_name(
    db: sqlalchemy.orm.Session, name: str
) -> typing.List[typing.Optional[w_type.WodType]]:
    db_wod_types: typing.List[typing.Optional[w_type.WodType]] = (
        db.query(w_type.WodType).filter(w_type.WodType.name.ilike(f"%{name}%")).all()
    )

    return db_wod_types


def get_type_by_id(db: sqlalchemy.orm.Session, type_id: int) -> w_type.WodType:
    db_type: w_type.WodType = db.get(w_type.WodType, type_id)

    if db_type is None:
        raise exceptions.UnknownWodType(type_id)

    return db_type
