from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User
from ..schemas import User
from ..utils.auth import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

@router.get("/", response_model=List[User])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    customers = db.query(User).filter(User.role == "customer").offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=User)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin" and current_user.id != customer_id:
        raise HTTPException(status_code=403, detail="Can only view your own profile")
    customer = db.query(User).filter(User.id == customer_id, User.role == "customer").first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}/activate")
def activate_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    customer = db.query(User).filter(User.id == customer_id, User.role == "customer").first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.is_active = True
    db.commit()
    return {"message": "Customer activated successfully"}

@router.put("/{customer_id}/deactivate")
def deactivate_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    customer = db.query(User).filter(User.id == customer_id, User.role == "customer").first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.is_active = False
    db.commit()
    return {"message": "Customer deactivated successfully"}
