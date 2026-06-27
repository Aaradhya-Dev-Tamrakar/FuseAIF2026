from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/orderdetails", tags=["Order Details"])

@router.get("/", response_model=list[schemas.OrderDetailOut])
def list_order_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_order_details(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.OrderDetailOut)
def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return crud.create_order_detail(db, order_detail)

@router.get("/{order_id}/{product_code}", response_model=schemas.OrderDetailOut)
def get_order_detail(order_id: int, product_code: str, db: Session = Depends(get_db)):
    order_detail = crud.get_order_detail(db, order_id, product_code)
    if not order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    return order_detail

@router.put("/{order_id}/{product_code}", response_model=schemas.OrderDetailOut)
def update_order_detail(order_id: int, product_code: str, order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    db_order_detail = crud.update_order_detail(db, order_id, product_code, order_detail)
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    return db_order_detail

@router.delete("/{order_id}/{product_code}")
def delete_order_detail(order_id: int, product_code: str, db: Session = Depends(get_db)):
    db_order_detail = crud.delete_order_detail(db, order_id, product_code)
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    return {"message": "Order Detail deleted"}
