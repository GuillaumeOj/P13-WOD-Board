import datetime
import typing

from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import user as user_crud
from wod_board.models import user as user_models


PASSWORD_CTXT = CryptContext(schemes=config.HASH_SCHEMES, deprecated="auto")

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=config.ACCESS_TOKEN_URL)


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


def get_user_with_token(
    db: sqlalchemy.orm.Session, token: str
) -> typing.Optional[user_models.User]:
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ACCESS_TOKEN_ALGORITHM]
        )
    except JWTError:
        return None

    username: str = payload.get("sub")
    if username is None:
        return None

    user = user_crud.get_user_by_email(db, user_email=username)
    if user is None:
        return None

    return user


def authenticate_user(
    db: sqlalchemy.orm.Session, email: str, password: str
) -> typing.Optional[user_models.User]:
    user = user_crud.get_user_by_email(db, email)

    if not user:
        return None

    if not PASSWORD_CTXT.verify(password, user.hashed_password):
        return None

    return user
