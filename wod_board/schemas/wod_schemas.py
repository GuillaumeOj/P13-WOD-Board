# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import datetime
import typing

from wod_board.schemas import OrmBase
from wod_board.schemas import round_schemas


class WodBase(OrmBase):
    description: typing.Optional[str]
    note: typing.Optional[str]
    date: datetime.datetime = datetime.datetime.utcnow()


class WodCreate(WodBase):
    wod_type: WodTypeCreate


class Wod(WodBase):
    id: int
    wod_type_id: int
    wod_type: WodType
    rounds: typing.List[round_schemas.Round]


class WodTypeBase(OrmBase):
    name: str


class WodTypeCreate(WodTypeBase):
    pass


class WodType(WodTypeBase):
    id: int


WodCreate.update_forward_refs()
Wod.update_forward_refs()
