import typing

from wod_board.schemas import OrmBase
from wod_board.schemas import equipment_schemas
from wod_board.schemas import movement_schemas


class GoalBase(OrmBase):
    movement_id: int
    round_id: int
    repetition: typing.Optional[int]
    duration_seconds: typing.Optional[int]


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: int
    movement: movement_schemas.Movement
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]]
