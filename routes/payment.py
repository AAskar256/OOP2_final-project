from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas import PaymentCreate, Payment
from crud import payments
from database import get_db

router = APIRouter()

@router.post("/", response_model=Payment, status_code=status.HTTP_201_CREATED)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return payments.make_payment(db, data)

@router.get("/{ticket_no}", response_model=Payment)
def get_payment(ticket_no: str, db: Session = Depends(get_db)):
    payment = payments.get_payment_by_ticket(db, ticket_no)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.delete("/{ticket_no}", status_code=status.HTTP_200_OK)
def delete_payment(ticket_no: str, db: Session = Depends(get_db)):
    return payments.delete_payment(ticket_no, db)