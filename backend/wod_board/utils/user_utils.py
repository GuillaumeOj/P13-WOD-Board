import datetime
import typing

import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
from jose import jwt
from jose.exceptions import JWTError
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import user_crud
from wod_board.models import get_db
from wod_board.models import user
from wod_board.schemas import user_schemas


class InvalidToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


# NOTE: https://github.com/mpdavis/python-jose/issues/215
# Jose does not provide type hints.
def create_access_token(
    user_account: user.User,
    expires_delta: typing.Optional[datetime.timedelta] = None,
) -> user_schemas.Token:
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"sub": user_account.email, "exp": expire}

    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=config.ACCESS_TOKEN_ALGORITHM
    )

    return user_schemas.Token(access_token=encoded_jwt, token_type="bearer")


def get_user_with_token(
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(config.OAUTH2_SCHEME),
) -> user.User:
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ACCESS_TOKEN_ALGORITHM],
        )
    except JWTError:
        raise InvalidToken

    email: str = payload.get("sub")

    try:
        return user_crud.get_user_by_email(db, email)
    except user_crud.UnknownUser:
        raise InvalidToken
