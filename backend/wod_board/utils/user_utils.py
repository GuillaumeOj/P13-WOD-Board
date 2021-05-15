import datetime
import typing

import daiquiri
import fastapi
from jose import jwt
from jose.exceptions import JWTError
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import user_crud
from wod_board.models import get_db
from wod_board.models import user
from wod_board.schemas import user_schemas


LOG = daiquiri.getLogger(__name__)


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

    return user_schemas.Token(access_token=encoded_jwt)


def get_user_with_token(
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(config.OAUTH2_SCHEME),
) -> user_schemas.User:
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ACCESS_TOKEN_ALGORITHM],
        )
    except JWTError:
        error = exceptions.InvalidToken(token)
        LOG.error(error)
        raise exceptions.RouterException(error)

    email: str = payload.get("sub")

    try:
        return user_schemas.User.from_orm(user_crud.get_user_by_email(db, email))
    except exceptions.UnknownUser:
        error = exceptions.InvalidToken(token)
        LOG.error(error)
        raise exceptions.RouterException(error)
