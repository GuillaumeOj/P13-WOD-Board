import typing

import daiquiri
import pydantic

from wod_board.schemas import OrmBase
from wod_board.schemas import equipment_schemas
from wod_board.schemas import unit_schemas


LOG = daiquiri.getLogger(__name__)


class MovementBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)
    unit_id: typing.Optional[int]


class MovementCreate(MovementBase):
    pass


class Movement(MovementBase):
    id: int
    unit: typing.Optional[unit_schemas.Unit]
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]]


class MovementGoalBase(OrmBase):
    movement_id: int
    round_id: int
    repetition: typing.Optional[int]
    duration_seconds: typing.Optional[int]


class MovementGoalCreate(MovementGoalBase):
    pass


class MovementGoal(MovementGoalBase):
    id: int
    movement: Movement
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]]
