import typing

import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import wod_round
from wod_board.utils import round_utils


def check_goal_author(
    db: sqlalchemy.orm.Session,
    round_id: int,
    user_id: int,
) -> None:
    db_round: typing.Optional[wod_round.Round] = db.get(wod_round.Round, round_id)

    if db_round is None:
        raise exceptions.UnknownRound(str(round_id))

    round_utils.check_round_author(db, db_round.wod_id, user_id)
