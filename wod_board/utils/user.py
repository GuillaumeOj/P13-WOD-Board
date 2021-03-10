import datetime
import typing

from jose import jwt
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import user as user_crud
from wod_board.models import user as user_models


def create_access_token(
    data: typing.Dict[str, typing.Any],
    expires_delta: typing.Optional[datetime.timedelta] = None,
) -> jwt.encode:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=config.ACCESS_TOKEN_ALGORITHM
    )

    return encoded_jwt


def authenticate_user(
    db: sqlalchemy.orm.Session, email: str, password: str
) -> typing.Optional[user_models.User]:
    user = user_crud.get_user_by_email(db, email)

    if not user:
        return None

    if not config.PASSWORD_CTXT.verify(password, user.hashed_password):
        return None

    return user
