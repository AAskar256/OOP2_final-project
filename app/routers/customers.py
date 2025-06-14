from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User as UserModel
from ..schemas import User as UserSchema
from ..utils.auth import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)


def get_customer_or_404(db: Session, customer_id: int) -> UserModel:
    customer = db.query(UserModel).filter(UserModel.id == customer_id, UserModel.role == "customer").first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@router.get("/", response_model=List[UserSchema])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    return db.query(UserModel).filter(UserModel.role == "customer").offset(skip).limit(limit).all()

@router.get("/{customer_id}", response_model=UserSchema)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    customer = get_customer_or_404(db, customer_id)
    if current_user.role != "admin" and current_user.id != customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this profile.")
    return customer

@router.put("/{customer_id}/activate", response_model=UserSchema)
def activate_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    customer = get_customer_or_404(db, customer_id)
    customer.is_active = True
    db.commit()
    db.refresh(customer)
    return customer

@router.put("/{customer_id}/deactivate", response_model=UserSchema)
def deactivate_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    customer = get_customer_or_404(db, customer_id)
    customer.is_active = False
    db.commit()
    db.refresh(customer)
    return customer
