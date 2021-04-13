import typing

import pydantic

from wod_board.schemas import OrmBase
from wod_board.schemas import equipment_schemas
from wod_board.schemas import unit_schemas


class MovementBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)
    unit_id: typing.Optional[int]


class MovementCreate(MovementBase):
    unit: typing.Optional[unit_schemas.UnitCreate]
    equipments: typing.Optional[typing.List[equipment_schemas.EquipmentCreate]]


class Movement(MovementBase):
    id: int
    unit: typing.Optional[unit_schemas.Unit]
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]]


class MovementGoalBase(OrmBase):
    movement_id: typing.Optional[int]
    repetition: typing.Optional[int]


class MovementGoalCreate(MovementGoalBase):
    id: typing.Optional[int]
    movement: MovementCreate
    equipments: typing.Optional[typing.List[equipment_schemas.EquipmentCreate]]

    @pydantic.validator("equipments", always=True, pre=True)
    def check_equipments(cls, v, values):
        movement = values.get("movement")
        if not v:
            return v
        for equipment in v:
            if not movement.equipments:
                raise ValueError(f"{equipment} is not in {movement.equipments}")
            if equipment not in movement.equipments:
                raise ValueError(f"{equipment} is not in {movement.equipments}")

        return v


class MovementGoal(MovementGoalBase):
    id: int
    movement: Movement
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]]
