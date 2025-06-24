from sqlalchemy.orm import Session
from models import Payment
from schemas import PaymentCreate
import uuid
from fastapi import HTTPException

def make_payment(db: Session, payment: PaymentCreate):
    existing = db.query(Payment).filter(Payment.TicketNo == payment.TicketNo).first()
    if existing:
        raise HTTPException(status_code=400, detail="Payment already exists for this ticket.")

    receipt = str(uuid.uuid4())[:8]
    new_payment = Payment(**payment.dict(), status="completed", receipt_no=receipt)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

def get_payment_by_ticket(db: Session, ticket_no: str):
    return db.query(Payment).filter(Payment.TicketNo == ticket_no).first()

def get_all_payments(db: Session):
    return db.query(Payment).all()

def delete_payment(ticket_no: str, db: Session):
    payment = db.query(Payment).filter(Payment.TicketNo == ticket_no).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"detail": "Payment deleted successfully"}