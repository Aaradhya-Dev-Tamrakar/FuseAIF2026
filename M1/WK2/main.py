from fastapi import FastAPI
from app import router as customers_router
from app import stats_router
from app import orders_router
from app import payments_router
from app import productlines_router
from app import products_router
from app import offices_router
from app import employees_router
from app import orderdetails_router
from app.logger import logger

app = FastAPI(title="Classical Models API")

logger.info("Application started")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Classical Models API!"}

app.include_router(customers_router.router)
app.include_router(orders_router.router)
app.include_router(payments_router.router)
app.include_router(productlines_router.router)
app.include_router(products_router.router)
app.include_router(offices_router.router)
app.include_router(employees_router.router)
app.include_router(orderdetails_router.router)
app.include_router(stats_router.router)
