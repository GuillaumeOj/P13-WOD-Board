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
    wod_type_id: typing.Optional[int]


class WodCreate(WodBase):
    wod_type: WodTypeCreate


class Wod(WodBase):
    id: int
    wod_type: WodType
    rounds: "typing.List[Round]"


class WodTypeBase(OrmBase):
    name: str


class WodTypeCreate(WodTypeBase):
    pass


class WodType(WodTypeBase):
    id: int


from wod_board.schemas.round_schemas import Round  # noqa


WodCreate.update_forward_refs()
Wod.update_forward_refs()
