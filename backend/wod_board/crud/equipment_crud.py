import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import equipment
from wod_board.schemas import equipment_schemas


LOG = daiquiri.getLogger(__name__)


def create_equipment(
    db: sqlalchemy.orm.Session,
    equiment_data: equipment_schemas.EquipmentCreate,
) -> equipment.Equipment:
    new_equipment = equipment.Equipment(**equiment_data.dict())

    db.add(new_equipment)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'duplicate key value violates unique constraint "equipment_name_key"'
            in str(error)
        ):
            raise exceptions.NameAlreadyUsed(equiment_data.name)

        LOG.error(str(error))

    db.refresh(new_equipment)

    return new_equipment


def get_equipment_by_name(
    db: sqlalchemy.orm.Session,
    name: str,
) -> equipment.Equipment:
    db_equiment: typing.Optional[equipment.Equipment] = (
        db.query(equipment.Equipment).filter(equipment.Equipment.name == name).first()
    )

    if db_equiment is None:
        raise exceptions.UnknownEquipment(name)

    return db_equiment
