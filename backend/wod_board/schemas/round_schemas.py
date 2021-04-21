# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import typing

from wod_board.schemas import OrmBase
from wod_board.schemas import movement_schemas


class RoundBase(OrmBase):
    position: int
    duration_seconds: typing.Optional[int]
    repetition: typing.Optional[int]
    wod_id: int


class RoundCreate(RoundBase):
    sub_rounds: typing.Optional[typing.List[RoundCreate]]
    movements: typing.Optional[typing.List[movement_schemas.MovementGoalCreate]]


class Round(RoundBase):
    id: int
    parent_id: typing.Optional[int]

    sub_rounds: typing.Optional[typing.List[Round]]
    movements: typing.Optional[typing.List[movement_schemas.MovementGoal]]


RoundCreate.update_forward_refs()
Round.update_forward_refs()
