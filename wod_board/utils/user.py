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
from wod_board.schemas import user as user_schemas


PASSWORD_CTXT = CryptContext(schemes=config.HASH_SCHEMES, deprecated="auto")

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=config.ACCESS_TOKEN_URL)


# NOTE: https://github.com/mpdavis/python-jose/issues/215
# Jose does not provide type hints.
def create_access_token(
    user: user_models.User,
    expires_delta: typing.Optional[datetime.timedelta] = None,
) -> user_schemas.Token:
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"sub": user.email, "exp": expire}

    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=config.ACCESS_TOKEN_ALGORITHM
    )

    return user_schemas.Token(access_token=encoded_jwt, token_type="bearer")


def get_user_with_token(
    db: sqlalchemy.orm.Session, token: user_schemas.Token
) -> typing.Optional[user_models.User]:
    try:
        payload = jwt.decode(
            token.access_token,
            config.SECRET_KEY,
            algorithms=[config.ACCESS_TOKEN_ALGORITHM],
        )
    except JWTError:
        return None

    email: str = payload.get("sub")

    user = user_crud.get_user_by_email(db, user_email=email)
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
