import typing

import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.models import wod
from wod_board.schemas import wod_schemas


class DuplicatedWodType(Exception):
    pass


class UnknownWodType(Exception):
    pass


class DuplicatedRoundPosition(Exception):
    pass


def _create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod_schemas.WodType:
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

    return wod_schemas.WodType.from_orm(new_type)


def _get_wod_type_by_name(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod_schemas.WodType:
    db_wod_type = (
        db.query(wod.WodType).filter(wod.WodType.name == wod_type.name).first()
    )

    if db_wod_type is None:
        raise UnknownWodType

    return wod_schemas.WodType.from_orm(db_wod_type)


def get_or_create_wod_type(
    db: sqlalchemy.orm.Session, wod_type: wod_schemas.WodTypeCreate
) -> wod_schemas.WodType:
    try:
        db_wod_type = _get_wod_type_by_name(db, wod_type)
    except UnknownWodType:
        db_wod_type = _create_wod_type(db, wod_type)

    return wod_schemas.WodType.from_orm(db_wod_type)


def create_rounds(
    db: sqlalchemy.orm.Session,
    rounds: typing.List[wod_schemas.RoundCreate],
) -> typing.List[wod_schemas.Round]:
    new_rounds = []
    for wod_round in rounds:
        sub_rounds = []
        if wod_round.children:
            sub_rounds = create_rounds(db, wod_round.children)

        new_round = wod.Round(**wod_round.dict())
        new_round.children.append(sub_rounds)

        db.add(new_round)
        try:
            db.commit()
        except sqlalchemy.exc.IntegrityError as error:
            db.rollback()
            if (
                'duplicate key value violates unique constraint "wod_id_position"'
                in str(error)
            ):
                raise DuplicatedRoundPosition

            raise error
        else:
            db.refresh(new_round)

        new_rounds.append(wod_schemas.Round.from_orm(new_round))

    return new_rounds


def create_wod(
    db: sqlalchemy.orm.Session,
    wod_data: wod_schemas.WodCreate,
) -> wod_schemas.Wod:

    wod_type = get_or_create_wod_type(db, wod_data.wod_type)

    new_wod = wod.Wod(
        wod_type.id,
        wod_data.description,
        wod_data.note,
        wod_data.date,
    )

    db.add(new_wod)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        raise error
    else:
        db.refresh(new_wod)

    return wod_schemas.Wod.from_orm(new_wod)
