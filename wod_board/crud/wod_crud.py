import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.models import wod
from wod_board.schemas import wod_schemas


class DuplicatedWodType(Exception):
    pass


class UnknownWodType(Exception):
    pass


class DuplicatedPosition(Exception):
    pass


def create_round(
    db: sqlalchemy.orm.Session, round_data: wod_schemas.Round
) -> wod.Round:
    new_round = wod.Round(
        position=round_data.position,
        duration_seconds=round_data.duration_seconds,
    )
    db.add(new_round)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if 'duplicate key value violates unique constraint "wod_id_position"' in str(
            error
        ):
            raise DuplicatedPosition
        else:
            raise error
    else:
        db.refresh(new_round)

    return new_round


def _create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodType
) -> wod.WodType:
    new_type = wod.WodType(name=wod_type.name)
    db.add(new_type)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if 'duplicate key value violates unique constraint "wod_type_name_key"' in str(
            error
        ):
            raise DuplicatedWodType
    else:
        db.refresh(new_type)

    return new_type


def _get_wod_type_by_name(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodType
) -> wod.WodType:
    db_wod_type = (
        db.query(wod.WodType).filter(wod.WodType.name == wod_type.name).first()
    )

    if db_wod_type is None:
        raise UnknownWodType

    return db_wod_type  # type: ignore[no-any-return]


def get_or_create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodType
) -> wod.WodType:
    try:
        db_wod_type = _get_wod_type_by_name(db, wod_type)
    except UnknownWodType:
        db_wod_type = _create_wod_type(db, wod_type)

    return db_wod_type


def create_wod(db: sqlalchemy.orm.Session, wod_data: wod_schemas.Wod) -> wod.Wod:
    wod_type = get_or_create_wod_type(db, wod_data.wod_type)

    new_wod = wod.Wod(
        description=wod_data.description,
        note=wod_data.note,
        date=wod_data.date,
        wod_type_id=wod_type.id,
    )

    for wod_round in wod_data.rounds:
        new_round = wod.Round(
            position=wod_round.position, duration_seconds=wod_round.duration_seconds
        )
        new_wod.rounds.append(new_round)
    db.add(new_wod)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
    else:
        db.refresh(new_wod)

    return new_wod
