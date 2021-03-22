import typing

import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.models import user
from wod_board.schemas import user_schemas
from wod_board.utils import user_utils


class DuplicatedEmail(Exception):
    pass


class DuplicatedUsername(Exception):
    pass


def get_user(db: sqlalchemy.orm.Session, user_id: int) -> typing.Optional[user.User]:
    return db.query(user.User).filter(user.User.id == user_id).first()


def get_user_by_email(
    db: sqlalchemy.orm.Session, user_email: str
) -> typing.Optional[user.User]:
    return db.query(user.User).filter(user.User.email == user_email).first()


def create_user(
    db: sqlalchemy.orm.Session, user_data: user_schemas.UserCreate
) -> user.User:
    hashed_password = user_utils.PASSWORD_CTXT.hash(user_data.password)

    new_user = user.User(
        email=user_data.email,
        hashed_password=hashed_password,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )

    db.add(new_user)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if 'duplicate key value violates unique constraint "user_email_key"' in str(
            error
        ):
            raise DuplicatedEmail
        elif (
            'duplicate key value violates unique constraint "user_username_key"'
        ) in str(error):
            raise DuplicatedUsername
    else:
        db.refresh(new_user)

    return new_user
