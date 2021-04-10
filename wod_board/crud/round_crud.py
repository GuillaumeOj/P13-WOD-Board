import typing

import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.models import wod_round
from wod_board.schemas import round_schemas


class DuplicatedRoundPosition(Exception):
    pass


class WrongWodId(Exception):
    pass


class UnknownRound(Exception):
    pass


def get_round_by_id(
    db: sqlalchemy.orm.Session,
    id: int,
) -> wod_round.Round:
    wanted_round: wod_round.Round = db.get(wod_round.Round, id)

    if wanted_round is None:
        raise UnknownRound

    return wanted_round


def create_round(
    db: sqlalchemy.orm.Session,
    round_data: round_schemas.RoundCreate,
    parent_id: typing.Optional[int] = None,
) -> wod_round.Round:
    new_round = wod_round.Round(
        position=round_data.position,
        duration_seconds=round_data.duration_seconds,
        wod_id=round_data.wod_id,
        parent_id=parent_id,
    )

    db.add(new_round)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if 'duplicate key value violates unique constraint "wod_id_position"' in str(
            error
        ):
            raise DuplicatedRoundPosition
        if (
            'insert or update on table "round" violates foreign '
            'key constraint "round_wod_id_fkey"'
        ) in str(error):
            raise WrongWodId

        raise error

    db.refresh(new_round)

    if round_data.children:
        for child in round_data.children:
            create_round(db, child, parent_id=new_round.id)

    db.refresh(new_round)

    return new_round
