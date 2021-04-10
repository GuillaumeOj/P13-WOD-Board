# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import typing

from wod_board.schemas import OrmBase


class RoundBase(OrmBase):
    position: int
    duration_seconds: int = 0
    wod_id: int


class RoundCreate(RoundBase):
    children: typing.Optional[typing.List[RoundCreate]] = None


class Round(RoundBase):
    id: int
    parent_id: typing.Optional[int]

    children: typing.Optional[typing.List[Round]] = None


RoundCreate.update_forward_refs()
Round.update_forward_refs()
