from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models.supply import Supply
from app.schemas.supply import SupplyCreate, SupplyUpdate

def create_supply(db: Session, supply_in: SupplyCreate) -> Supply:
    db_supply = Supply(**supply_in.model_dump())
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return db_supply

def get_supplies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Supply).offset(skip).limit(limit).all()

def get_supply(db: Session, supply_id: UUID):
    return db.query(Supply).filter(Supply.id == supply_id).first()

def update_supply(db: Session, supply_id: UUID, supply_in: SupplyUpdate):
    db_supply = get_supply(db, supply_id)
    if not db_supply:
        return None
    for field, value in supply_in.model_dump(exclude_unset=True).items():
        setattr(db_supply, field, value)
    db.commit()
    db.refresh(db_supply)
    return db_supply

def delete_supply(db: Session, supply_id: UUID):
    db_supply = get_supply(db, supply_id)
    if not db_supply:
        return None
    db.delete(db_supply)
    db.commit()
    return db_supply
