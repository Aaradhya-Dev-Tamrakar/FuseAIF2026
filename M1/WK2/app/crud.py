# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app import models, schemas
from app.logger import logger

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching customers — skip = {skip}, limit = {limit}")
    return db.query(models.Customer).offset(skip).limit(limit).all()

def get_customer(db: Session, customer_id: int):
    logger.info(f"Fetching customer {customer_id}")
    return db.query(models.Customer).filter(models.Customer.customerNumber == customer_id).first()

def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    logger.info(f"Creating customer with name {customer.customerName}")
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db, customer_id, customer: schemas.CustomerUpdate) -> models.Customer:
    logger.info(f"Updating customer {customer_id}")
    db_customer = get_customer(db, customer_id)
    for key, value in customer.model_dump(exclude_unset = True).items():
        setattr(db_customer,key,value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db, customer_id):
    logger.info(f"Deleting customer {customer_id}")
    db_customer = get_customer(db,customer_id)
    db.delete(db_customer)
    db.commit()
    return db_customer

def get_customer_orders(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching orders for customer {customer_id} — skip = {skip}, limit = {limit}")
    return db.query(models.Order).filter(models.Order.customerNumber == customer_id).offset(skip).limit(limit).all()

def get_customer_payments(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching payments for customer {customer_id} — skip = {skip}, limit = {limit}")
    return db.query(models.Payment).filter(models.Payment.customerNumber == customer_id).offset(skip).limit(limit).all()

# --- Orders CRUD ---
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.orderNumber == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate) -> models.Order:
    db_order = get_order(db, order_id)
    for key, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    db.delete(db_order)
    db.commit()
    return db_order

# --- Payments CRUD ---
def get_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Payment).offset(skip).limit(limit).all()

def get_payment(db: Session, customer_id: int, check_number: str):
    return db.query(models.Payment).filter(models.Payment.customerNumber == customer_id, models.Payment.checkNumber == check_number).first()

def create_payment(db: Session, payment: schemas.PaymentCreate) -> models.Payment:
    db_payment = models.Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment(db: Session, customer_id: int, check_number: str, payment: schemas.PaymentUpdate) -> models.Payment:
    db_payment = get_payment(db, customer_id, check_number)
    for key, value in payment.model_dump(exclude_unset=True).items():
        setattr(db_payment, key, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, customer_id: int, check_number: str):
    db_payment = get_payment(db, customer_id, check_number)
    db.delete(db_payment)
    db.commit()
    return db_payment

# --- ProductLines CRUD ---
def get_product_lines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProductLine).offset(skip).limit(limit).all()

def get_product_line(db: Session, product_line_id: str):
    return db.query(models.ProductLine).filter(models.ProductLine.productLine == product_line_id).first()

def create_product_line(db: Session, product_line: schemas.ProductLineCreate) -> models.ProductLine:
    db_product_line = models.ProductLine(**product_line.model_dump())
    db.add(db_product_line)
    db.commit()
    db.refresh(db_product_line)
    return db_product_line

def update_product_line(db: Session, product_line_id: str, product_line: schemas.ProductLineUpdate) -> models.ProductLine:
    db_product_line = get_product_line(db, product_line_id)
    for key, value in product_line.model_dump(exclude_unset=True).items():
        setattr(db_product_line, key, value)
    db.commit()
    db.refresh(db_product_line)
    return db_product_line

def delete_product_line(db: Session, product_line_id: str):
    db_product_line = get_product_line(db, product_line_id)
    db.delete(db_product_line)
    db.commit()
    return db_product_line

# --- Products CRUD ---
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_code: str):
    return db.query(models.Product).filter(models.Product.productCode == product_code).first()

def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_code: str, product: schemas.ProductUpdate) -> models.Product:
    db_product = get_product(db, product_code)
    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_code: str):
    db_product = get_product(db, product_code)
    db.delete(db_product)
    db.commit()
    return db_product

# --- Offices CRUD ---
def get_offices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Office).offset(skip).limit(limit).all()

def get_office(db: Session, office_code: str):
    return db.query(models.Office).filter(models.Office.officeCode == office_code).first()

def create_office(db: Session, office: schemas.OfficeCreate) -> models.Office:
    db_office = models.Office(**office.model_dump())
    db.add(db_office)
    db.commit()
    db.refresh(db_office)
    return db_office

def update_office(db: Session, office_code: str, office: schemas.OfficeUpdate) -> models.Office:
    db_office = get_office(db, office_code)
    for key, value in office.model_dump(exclude_unset=True).items():
        setattr(db_office, key, value)
    db.commit()
    db.refresh(db_office)
    return db_office

def delete_office(db: Session, office_code: str):
    db_office = get_office(db, office_code)
    db.delete(db_office)
    db.commit()
    return db_office

# --- Employees CRUD ---
def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.employeeNumber == employee_id).first()

def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate) -> models.Employee:
    db_employee = get_employee(db, employee_id)
    for key, value in employee.model_dump(exclude_unset=True).items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    db.delete(db_employee)
    db.commit()
    return db_employee

# --- OrderDetails CRUD ---
def get_order_details(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OrderDetail).offset(skip).limit(limit).all()

def get_order_detail(db: Session, order_id: int, product_code: str):
    return db.query(models.OrderDetail).filter(models.OrderDetail.orderNumber == order_id, models.OrderDetail.productCode == product_code).first()

def create_order_detail(db: Session, order_detail: schemas.OrderDetailCreate) -> models.OrderDetail:
    db_order_detail = models.OrderDetail(**order_detail.model_dump())
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def update_order_detail(db: Session, order_id: int, product_code: str, order_detail: schemas.OrderDetailUpdate) -> models.OrderDetail:
    db_order_detail = get_order_detail(db, order_id, product_code)
    for key, value in order_detail.model_dump(exclude_unset=True).items():
        setattr(db_order_detail, key, value)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def delete_order_detail(db: Session, order_id: int, product_code: str):
    db_order_detail = get_order_detail(db, order_id, product_code)
    db.delete(db_order_detail)
    db.commit()
    return db_order_detail
