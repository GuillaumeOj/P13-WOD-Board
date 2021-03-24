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
    rounds: typing.List[RoundCreate]
    wod_type: WodTypeCreate


class Wod(WodBase):
    id: int
    rounds: typing.List[Round]
    wod_type: WodType


class WodTypeBase(OrmBase):
    name: str


class WodTypeCreate(WodTypeBase):
    pass


class WodType(WodTypeBase):
    id: int


class RoundBase(OrmBase):
    position: int
    duration_seconds: int = 0


class RoundCreate(RoundBase):
    pass


class Round(RoundBase):
    id: int
    wod_id: int


WodCreate.update_forward_refs()
Wod.update_forward_refs()
