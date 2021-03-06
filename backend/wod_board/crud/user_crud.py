import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import user
from wod_board.schemas import user_schemas


LOG = daiquiri.getLogger(__name__)


def create_user(
    db: sqlalchemy.orm.Session, user_data: user_schemas.UserCreate
) -> user.User:
    new_user = user.User(**user_data.dict())

    db.add(new_user)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if 'duplicate key value violates unique constraint "user_email_key"' in str(
            error
        ):
            raise exceptions.DuplicatedEmail
        if (
            'duplicate key value violates unique constraint "user_username_key"'
        ) in str(error):
            raise exceptions.DuplicatedUsername

        LOG.error(error)
    else:
        db.refresh(new_user)

    return new_user


def get_user_by_id(db: sqlalchemy.orm.Session, id: int) -> user.User:
    db_user: user.User = db.get(user.User, id)

    if db_user is None:
        raise exceptions.UnknownUser

    return db_user


def get_user_by_email(db: sqlalchemy.orm.Session, email: str) -> user.User:
    db_user: typing.Optional[user.User] = (
        db.query(user.User).filter(user.User.email == email).first()
    )

    if db_user is None:
        raise exceptions.UnknownUser

    return db_user
