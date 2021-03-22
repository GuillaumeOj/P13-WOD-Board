import sqlalchemy
from sqlalchemy.ext import declarative
import sqlalchemy.orm

from wod_board import config


class SessionContext(sqlalchemy.orm.Session):
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()


class ModelBase:
    @property
    def session(self) -> sqlalchemy.orm.Session:
        return sqlalchemy.orm.object_session(self)  # type: ignore[no-any-return]


Base = declarative.declarative_base(cls=ModelBase)

engine = sqlalchemy.create_engine(config.DATABASE_URL)

Session = sqlalchemy.orm.sessionmaker(bind=engine, class_=SessionContext)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# Import each model fo Alembic
from wod_board.models.user import User  # noqa
from wod_board.models.wod import *  # noqa


def create_all() -> None:
    Base.metadata.create_all(bind=engine)


def drop_all() -> None:
    Base.metadata.drop_all(bind=engine)
