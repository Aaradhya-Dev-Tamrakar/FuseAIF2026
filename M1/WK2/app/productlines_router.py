from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/productlines", tags=["Product Lines"])

@router.get("/", response_model=list[schemas.ProductLineOut])
def list_product_lines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_product_lines(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.ProductLineOut)
def create_product_line(product_line: schemas.ProductLineCreate, db: Session = Depends(get_db)):
    return crud.create_product_line(db, product_line)

@router.get("/{product_line_id}", response_model=schemas.ProductLineOut)
def get_product_line(product_line_id: str, db: Session = Depends(get_db)):
    product_line = crud.get_product_line(db, product_line_id)
    if not product_line:
        raise HTTPException(status_code=404, detail="Product Line not found")
    return product_line

@router.put("/{product_line_id}", response_model=schemas.ProductLineOut)
def update_product_line(product_line_id: str, product_line: schemas.ProductLineUpdate, db: Session = Depends(get_db)):
    db_product_line = crud.update_product_line(db, product_line_id, product_line)
    if not db_product_line:
        raise HTTPException(status_code=404, detail="Product Line not found")
    return db_product_line

@router.delete("/{product_line_id}")
def delete_product_line(product_line_id: str, db: Session = Depends(get_db)):
    db_product_line = crud.delete_product_line(db, product_line_id)
    if not db_product_line:
        raise HTTPException(status_code=404, detail="Product Line not found")
    return {"message": "Product Line deleted"}
