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
            raise exceptions.UnknownWodType(str(wod_data.wod_type_id))
        if (
            'insert or update on table "wod" violates foreign '
            'key constraint "wod_author_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownUser(str(wod_data.author_id))
        if ('duplicate key value violates unique constraint "wod_title_key"') in str(
            error
        ):
            raise exceptions.TitleAlreadyUsed(wod_data.title)
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
        raise exceptions.UnknownWod(str(wod_id))

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
            raise exceptions.UnknownWodType(str(wod_data.wod_type_id))
        if (
            'insert or update on table "wod" violates foreign '
            'key constraint "wod_author_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownUser(str(wod_data.author_id))
        if ('duplicate key value violates unique constraint "wod_title_key"') in str(
            error
        ):
            raise exceptions.TitleAlreadyUsed(wod_data.title)
        LOG.error(error)

    db.refresh(db_wod)

    return db_wod


def get_wod_by_id(db: sqlalchemy.orm.Session, wod_id: int) -> wod.Wod:
    db_wod: typing.Optional[wod.Wod] = db.get(wod.Wod, wod_id)

    if db_wod is None:
        raise exceptions.UnknownWod(str(wod_id))

    return db_wod


def get_wod_incomplete(db: sqlalchemy.orm.Session, author_id: int) -> wod.Wod:
    db_wod: typing.Optional[wod.Wod] = (
        db.query(wod.Wod).filter_by(author_id=author_id, is_complete=False).first()
    )

    if db_wod is None:
        raise exceptions.UnknownWod("No incomplete wod found")

    return db_wod
