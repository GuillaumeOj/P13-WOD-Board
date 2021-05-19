# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import typing

from wod_board.schemas import OrmBase
from wod_board.schemas import goal_schemas


class RoundBase(OrmBase):
    position: int
    duration_seconds: int = 0
    repetition: int = 0
    wod_id: int
    parent_id: typing.Optional[int]


class RoundCreate(RoundBase):
    pass


class Round(RoundBase):
    id: int

    sub_rounds: typing.List[typing.Optional[Round]]
    goals: typing.List[typing.Optional[goal_schemas.Goal]]


RoundCreate.update_forward_refs()
Round.update_forward_refs()
