# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import datetime
import typing

from wod_board.schemas import OrmBase


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
    rounds: typing.List[Round]


class WodTypeBase(OrmBase):
    name: str


class WodTypeCreate(WodTypeBase):
    pass


class WodType(WodTypeBase):
    id: int


class RoundBase(OrmBase):
    position: int
    duration_seconds: int = 0
    wod_id: int


class RoundCreate(RoundBase):
    children: typing.Optional[typing.List[RoundCreate]]


class Round(RoundBase):
    id: int
    parent_id: typing.Optional[int]

    children: typing.Optional[typing.List[Round]]


WodCreate.update_forward_refs()
Wod.update_forward_refs()
RoundCreate.update_forward_refs()
Round.update_forward_refs()
