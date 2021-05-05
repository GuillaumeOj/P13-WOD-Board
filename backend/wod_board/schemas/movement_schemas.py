import typing

import pydantic

from wod_board.schemas import OrmBase
from wod_board.schemas import equipment_schemas
from wod_board.schemas import unit_schemas


class MovementBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)
    unit_id: int


class MovementCreate(MovementBase):
    pass


class Movement(MovementBase):
    id: int
    unit: unit_schemas.Unit
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]]
