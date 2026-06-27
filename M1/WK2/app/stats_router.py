import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/customers")
def stats_customers(db: Session = Depends(get_db)):
    count = db.query(models.Customer).count()
    return {"table": "customers", "count": count}

@router.get("/payments")
def stats_payments(db: Session = Depends(get_db)):
    count = db.query(models.Payment).count()
    return {"table": "payments", "count": count}

@router.get("/orders")
def stats_orders(db: Session = Depends(get_db)):
    count = db.query(models.Order).count()
    return {"table": "orders", "count": count}

@router.get("/orderdetails")
def stats_orderdetails(db: Session = Depends(get_db)):
    count = db.query(models.OrderDetail).count()
    return {"table": "orderdetails", "count": count}

@router.get("/productlines")
def stats_productlines(db: Session = Depends(get_db)):
    count = db.query(models.ProductLine).count()
    return {"table": "productlines", "count": count}

@router.get("/products")
def stats_products(db: Session = Depends(get_db)):
    count = db.query(models.Product).count()
    return {"table": "products", "count": count}

@router.get("/offices")
def stats_offices(db: Session = Depends(get_db)):
    count = db.query(models.Office).count()
    return {"table": "offices", "count": count}

@router.get("/employees")
def stats_employees(db: Session = Depends(get_db)):
    count = db.query(models.Employee).count()
    return {"table": "employees", "count": count}

@router.get("/")
async def stats_all(db: Session = Depends(get_db)):
    loop = asyncio.get_event_loop()

    async def count(fn):
        return await loop.run_in_executor(None, fn, db)

    (customers, payments, orders, orderdetails,
     productlines, products, offices, employees) = await asyncio.gather(
        count(lambda db: db.query(models.Customer).count()),
        count(lambda db: db.query(models.Payment).count()),
        count(lambda db: db.query(models.Order).count()),
        count(lambda db: db.query(models.OrderDetail).count()),
        count(lambda db: db.query(models.ProductLine).count()),
        count(lambda db: db.query(models.Product).count()),
        count(lambda db: db.query(models.Office).count()),
        count(lambda db: db.query(models.Employee).count()),
    )

    total = customers + payments + orders + orderdetails + productlines + products + offices + employees

    return {
        "tables": {
            "customers": customers,
            "payments": payments,
            "orders": orders,
            "orderdetails": orderdetails,
            "productlines": productlines,
            "products": products,
            "offices": offices,
            "employees": employees
        },
        "total_rows": total
    }
