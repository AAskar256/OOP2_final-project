from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import customers
from schemas import Customer, CustomerCreate
from database import get_db
from auth_utils import require_role

router = APIRouter()

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return customers.create_customer(db, customer)

@router.get("/", response_model=list[Customer], status_code=status.HTTP_200_OK)
def get_customers(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin"))
):
    return customers.get_customers(db)

@router.get("/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin"))
):
    customer = customers.get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}", status_code=status.HTTP_200_OK)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin"))
):
    return customers.delete_customer(db, customer_id)

@router.put("/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
def update_customer(
    customer_id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin"))
):
    return customers.update_customer(db, customer_id, customer)
