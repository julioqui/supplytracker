from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.db.crud import supplies as crud
from app.schemas.supply import SupplyCreate, SupplyUpdate, SupplyResponse

router = APIRouter(
    prefix="/supplies",
    tags=["supplies"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=SupplyResponse)
def create_supply(supply_in: SupplyCreate, db: Session = Depends(get_db)):
    return crud.create_supply(db, supply_in)

@router.get("/", response_model=List[SupplyResponse])
def read_supplies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_supplies(db, skip=skip, limit=limit)

@router.get("/{supply_id}", response_model=SupplyResponse)
def read_supply(supply_id: UUID, db: Session = Depends(get_db)):
    supply = crud.get_supply(db, supply_id)
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    return supply

@router.patch("/{supply_id}", response_model=SupplyResponse)
def update_supply(supply_id: UUID, supply_in: SupplyUpdate, db: Session = Depends(get_db)):
    supply = crud.update_supply(db, supply_id, supply_in)
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    return supply

@router.delete("/{supply_id}", response_model=SupplyResponse)
def delete_supply(supply_id: UUID, db: Session = Depends(get_db)):
    supply = crud.delete_supply(db, supply_id)
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    return supply
