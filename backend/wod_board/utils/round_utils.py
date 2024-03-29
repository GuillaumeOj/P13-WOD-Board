import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import wod


def check_round_author(
    db: sqlalchemy.orm.Session,
    wod_id: int,
    user_id: int,
) -> None:
    db_wod: wod.Wod = db.get(wod.Wod, wod_id)

    if db_wod is None:
        raise exceptions.UnknownWod(str(wod_id))

    if db_wod.author_id != user_id:
        raise exceptions.UserIsNotAuthor(str(user_id))
