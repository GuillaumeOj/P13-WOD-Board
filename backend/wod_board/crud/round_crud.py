import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.models import wod_round
from wod_board.schemas import round_schemas


LOG = daiquiri.getLogger(__name__)


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
        repetition=round_data.repetition,
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

    if round_data.sub_rounds:
        for sub_round in round_data.sub_rounds:
            create_round(db, sub_round, parent_id=new_round.id)
        db.refresh(new_round)

    return new_round


def update_round(
    db: sqlalchemy.orm.Session,
    round_data: round_schemas.RoundCreate,
    id: int,
    parent_id: typing.Optional[int] = None,
) -> wod_round.Round:
    db_round: wod_round.Round = db.get(wod_round.Round, id)

    if db_round is None:
        raise UnknownRound

    db_round.position = round_data.position
    db_round.duration_seconds = round_data.duration_seconds
    db_round.repetition = round_data.repetition
    db_round.wod_id = round_data.wod_id
    db_round.parent_id = parent_id

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

    db.refresh(db_round)

    if round_data.sub_rounds:
        for sub_round in round_data.sub_rounds:
            create_round(db, sub_round, parent_id=db_round.id)
        db.refresh(db_round)

    return db_round


def delete_round_by_id(
    db: sqlalchemy.orm.Session,
    id: int,
) -> bool:
    db_round = db.get(wod_round.Round, id)

    if db_round is None:
        raise UnknownRound

    db.delete(db_round)
    db.commit()

    return True
