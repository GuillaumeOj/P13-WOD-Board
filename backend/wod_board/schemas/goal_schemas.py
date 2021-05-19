import typing

from wod_board.schemas import OrmBase
from wod_board.schemas import equipment_schemas
from wod_board.schemas import movement_schemas


class GoalBase(OrmBase):
    movement_id: int
    round_id: int
    repetition: int = 0
    duration_seconds: int = 0


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: int
    movement: movement_schemas.Movement
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]]
