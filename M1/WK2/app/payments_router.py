from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/", response_model=list[schemas.PaymentOut])
def list_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_payments(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.PaymentOut)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db, payment)

@router.get("/{customer_id}/{check_number}", response_model=schemas.PaymentOut)
def get_payment(customer_id: int, check_number: str, db: Session = Depends(get_db)):
    payment = crud.get_payment(db, customer_id, check_number)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.put("/{customer_id}/{check_number}", response_model=schemas.PaymentOut)
def update_payment(customer_id: int, check_number: str, payment: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = crud.update_payment(db, customer_id, check_number, payment)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.delete("/{customer_id}/{check_number}")
def delete_payment(customer_id: int, check_number: str, db: Session = Depends(get_db)):
    db_payment = crud.delete_payment(db, customer_id, check_number)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted"}
