import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import config
from wod_board.models import user
from wod_board.schemas import user_schemas


LOG = daiquiri.getLogger(__name__)


class UnknownUser(Exception):
    pass


class DuplicatedEmail(Exception):
    pass


class DuplicatedUsername(Exception):
    pass


def create_user(
    db: sqlalchemy.orm.Session, user_data: user_schemas.UserCreate
) -> user.User:
    hashed_password = config.PASSWORD_CTXT.hash(user_data.password)

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
        if (
            'duplicate key value violates unique constraint "user_username_key"'
        ) in str(error):
            raise DuplicatedUsername

        LOG.error(error)
    else:
        db.refresh(new_user)

    return new_user


def get_user_by_id(db: sqlalchemy.orm.Session, id: int) -> user.User:
    db_user: user.User = db.get(user.User, id)

    if db_user is None:
        raise UnknownUser

    return db_user


def get_user_by_email(db: sqlalchemy.orm.Session, email: str) -> user.User:
    db_user: user.User = db.query(user.User).filter(user.User.email == email).first()

    if db_user is None:
        raise UnknownUser

    return db_user
