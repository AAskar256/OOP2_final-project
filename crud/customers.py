from sqlalchemy.orm import Session
from models import Customer
from schemas import CustomerCreate

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.CustomerId == customer_id).first()

def delete_customer(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.CustomerId == customer_id).first()
    if customer:
        db.delete(customer)
        db.commit()
    return customer

def update_customer(db: Session, customer_id: int, updated: CustomerCreate):
    customer = db.query(Customer).filter(Customer.CustomerId == customer_id).first()
    if customer:
        for key, value in updated.dict().items():
            setattr(customer, key, value)
        db.commit()
        db.refresh(customer)
    return customer
