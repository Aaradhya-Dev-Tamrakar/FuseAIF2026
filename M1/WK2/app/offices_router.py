from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/offices", tags=["Offices"])

@router.get("/", response_model=list[schemas.OfficeOut])
def list_offices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_offices(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.OfficeOut)
def create_office(office: schemas.OfficeCreate, db: Session = Depends(get_db)):
    return crud.create_office(db, office)

@router.get("/{office_code}", response_model=schemas.OfficeOut)
def get_office(office_code: str, db: Session = Depends(get_db)):
    office = crud.get_office(db, office_code)
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")
    return office

@router.put("/{office_code}", response_model=schemas.OfficeOut)
def update_office(office_code: str, office: schemas.OfficeUpdate, db: Session = Depends(get_db)):
    db_office = crud.update_office(db, office_code, office)
    if not db_office:
        raise HTTPException(status_code=404, detail="Office not found")
    return db_office

@router.delete("/{office_code}")
def delete_office(office_code: str, db: Session = Depends(get_db)):
    db_office = crud.delete_office(db, office_code)
    if not db_office:
        raise HTTPException(status_code=404, detail="Office not found")
    return {"message": "Office deleted"}
