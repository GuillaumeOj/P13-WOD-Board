import sqlalchemy.orm

from wod_board.crud import unit_crud
from wod_board.models import equipment
from wod_board.schemas import equipment_schemas


class UnknownEquipment(Exception):
    pass


def create_equipment(
    db: sqlalchemy.orm.Session,
    equiment_data: equipment_schemas.EquipmentCreate,
) -> equipment.Equipment:
    new_equipment = equipment.Equipment(name=equiment_data.name)

    if equiment_data.unit:
        new_equipment.unit = unit_crud.get_or_create_unit(db, equiment_data.unit)

    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)

    return new_equipment


def get_equipment_by_exact_name(
    db: sqlalchemy.orm.Session,
    name: str,
) -> equipment.Equipment:
    db_equiment: equipment.Equipment = (
        db.query(equipment.Equipment).filter(equipment.Equipment.name == name).first()
    )

    if db_equiment is None:
        raise UnknownEquipment

    return db_equiment


def get_or_create_equipment(
    db: sqlalchemy.orm.Session,
    equipment_data: equipment_schemas.EquipmentCreate,
) -> equipment.Equipment:
    try:
        db_equiment = get_equipment_by_exact_name(db, equipment_data.name)
    except UnknownEquipment:
        db_equiment = create_equipment(db, equipment_data)

    return db_equiment
