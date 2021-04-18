import sqlalchemy
from sqlalchemy.ext import declarative
import sqlalchemy.orm

from wod_board import config


class ModelBase:
    @property
    def session(self) -> sqlalchemy.orm.Session:
        return sqlalchemy.orm.object_session(self)  # type: ignore[no-any-return]


Base = declarative.declarative_base(cls=ModelBase)

engine = sqlalchemy.create_engine(config.DATABASE_URL)

Session = sqlalchemy.orm.sessionmaker(bind=engine, class_=sqlalchemy.orm.Session)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# Import each model fo Alembic
from wod_board.models.equipment import *  # noqa
from wod_board.models.movement import *  # noqa
from wod_board.models.unit import *  # noqa
from wod_board.models.user import *  # noqa
from wod_board.models.wod import *  # noqa
from wod_board.models.wod_round import *  # noqa


def create_all() -> None:
    Base.metadata.create_all(bind=engine)


def drop_all() -> None:
    Base.metadata.drop_all(bind=engine)
