import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import wod_round
from wod_board.schemas import round_schemas
from wod_board.utils import round_utils


LOG = daiquiri.getLogger(__name__)


def get_round_by_id(
    db: sqlalchemy.orm.Session,
    id: int,
) -> wod_round.Round:
    wanted_round: wod_round.Round = db.get(wod_round.Round, id)

    if wanted_round is None:
        raise exceptions.UnknownRound

    return wanted_round


def create_round(
    db: sqlalchemy.orm.Session,
    round_data: round_schemas.RoundCreate,
    user_id: int,
) -> wod_round.Round:
    round_utils.check_round_author(db, round_data.wod_id, user_id)

    new_round = wod_round.Round(**round_data.dict())

    db.add(new_round)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if 'duplicate key value violates unique constraint "wod_id_position"' in str(
            error
        ):
            raise exceptions.DuplicatedRoundPosition

        LOG.error(error)

    db.refresh(new_round)

    return new_round


def update_round(
    db: sqlalchemy.orm.Session,
    round_data: round_schemas.RoundCreate,
    round_id: int,
    user_id: int,
    parent_id: typing.Optional[int] = None,
) -> wod_round.Round:
    round_utils.check_round_author(db, round_data.wod_id, user_id)

    db_round: wod_round.Round = db.get(wod_round.Round, round_id)

    if db_round is None:
        raise exceptions.UnknownRound

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
            raise exceptions.DuplicatedRoundPosition

        LOG.error(error)

    db.refresh(db_round)

    return db_round


def delete_round_by_id(
    db: sqlalchemy.orm.Session,
    round_id: int,
    user_id: int,
) -> bool:
    db_round = db.get(wod_round.Round, round_id)

    if db_round is None:
        raise exceptions.UnknownRound

    round_utils.check_round_author(db, db_round.wod_id, user_id)

    db.delete(db_round)
    db.commit()

    return True
