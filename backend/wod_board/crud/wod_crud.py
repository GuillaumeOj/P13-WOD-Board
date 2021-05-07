import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import wod
from wod_board.schemas import wod_schemas


LOG = daiquiri.getLogger(__name__)


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
