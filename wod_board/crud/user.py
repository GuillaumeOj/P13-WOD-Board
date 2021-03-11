import typing

import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.models import user as user_models
from wod_board.schemas import user as user_schemas
from wod_board.utils import user as user_utils


class DuplicatedEmail(Exception):
    pass


class DuplicatedUsername(Exception):
    pass


def get_user(
    db: sqlalchemy.orm.Session, user_id: int
) -> typing.Optional[user_models.User]:
    return db.query(user_models.User).filter(user_models.User.id == user_id).first()


def get_user_by_email(
    db: sqlalchemy.orm.Session, user_email: str
) -> typing.Optional[user_models.User]:
    return (
        db.query(user_models.User).filter(user_models.User.email == user_email).first()
    )


def create_user(
    db: sqlalchemy.orm.Session, new_user: user_schemas.UserCreate
) -> user_models.User:
    hashed_password = user_utils.PASSWORD_CTXT.hash(new_user.password)

    user = user_models.User(
        email=new_user.email,
        hashed_password=hashed_password,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
    )

    db.add(user)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'duplicate key value violates unique constraint "wod_board_user_email_key"'
            in str(error)
        ):
            raise DuplicatedEmail
        elif (
            "duplicate key value violates unique constraint"
            ' "wod_board_user_username_key"'
        ) in str(error):
            raise DuplicatedUsername
    else:
        db.refresh(user)

    return user
