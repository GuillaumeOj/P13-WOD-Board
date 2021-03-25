import pydantic
import pytest

from wod_board.crud import wod_crud
from wod_board.models import wod
from wod_board.schemas import wod_schemas


def test_create_wod_type(db):
    wod_type_schema = wod_schemas.WodTypeBase(name="AMRAP")

    created_type = wod_crud._create_wod_type(db, wod_type_schema)
    assert created_type.name == wod_type_schema.name

    with pytest.raises(wod_crud.DuplicatedWodType):
        wod_crud._create_wod_type(db, wod_type_schema)

    types = db.query(wod.WodType).all()
    assert len(types) == 1


def test_get_wod_type_by_name(db):
    wod_type_schema = wod_schemas.WodTypeBase(name="AMRAP")
    wod_crud._create_wod_type(db, wod_type_schema)

    wod_type = wod_crud._get_wod_type_by_name(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name

    wod_type_schema = wod_schemas.WodTypeBase(name="For Time")
    with pytest.raises(wod_crud.UnknownWodType):
        wod_type = wod_crud._get_wod_type_by_name(db, wod_type_schema)


def test_get_or_create_wod_type(db):
    wod_type_schema = wod_schemas.WodTypeBase(name="AMRAP")

    wod_type = wod_crud.get_or_create_wod_type(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name

    wod_type = wod_crud.get_or_create_wod_type(db, wod_type_schema)
    assert wod_type.name == wod_type_schema.name

    wod_types = db.query(wod.WodType).all()
    assert len(wod_types) == 1


def test_create_wod(db):
    wod_type_schema = wod_schemas.WodTypeBase(name="AMRAP")

    round_parent = wod_schemas.RoundBase(position=1)
    round_child_1 = wod_schemas.RoundBase(
        position=2, duration_seconds=20, parent=round_parent
    )
    round_child_2 = wod_schemas.RoundBase(
        position=3, duration_seconds=10, parent=round_parent
    )

    wod_schema = wod_schemas.WodCreate(
        description="Foo WOD",
        note="",
        wod_type=wod_type_schema,
        rounds=[round_parent, round_child_1, round_child_2],
    )

    new_wod = wod_crud.create_wod(db, wod_schema)
    assert new_wod.rounds.count() == 3

    wods = db.query(wod.Wod).all()
    assert len(wods) == 1


def test_create_wod_with_duplicated_round_position(db):
    wod_type_schema = wod_schemas.WodTypeBase(name="AMRAP")

    round_parent = wod_schemas.RoundBase(position=1)
    round_child_1 = wod_schemas.RoundBase(
        position=1, duration_seconds=20, parent=round_parent
    )

    with pytest.raises(pydantic.ValidationError):
        wod_schemas.WodCreate(
            description="Foo WOD",
            note="",
            wod_type=wod_type_schema,
            rounds=[round_parent, round_child_1],
        )
