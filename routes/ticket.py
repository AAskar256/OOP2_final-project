from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Ticket, TicketCreate
from crud import tickets
from auth_utils import get_current_user, require_role
from models import User

router = APIRouter()

@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(data: TicketCreate, db: Session = Depends(get_db)):
    return tickets.create_ticket(db, data)

@router.get("/", response_model=list[Ticket])
def get_all_tickets(
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin"))
):
    return tickets.get_all_tickets(db)

@router.get("/{ticket_no}", response_model=Ticket)
def get_ticket(
    ticket_no: str,
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin"))
):
    t = tickets.get_ticket_by_number(db, ticket_no)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t

@router.delete("/{ticket_no}", status_code=status.HTTP_200_OK)
def cancel_ticket(
    ticket_no: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = tickets.get_ticket_by_number(db, ticket_no)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Check if the ticket belongs to the logged-in user
    customer = db.query(models.Customer).filter(models.Customer.Email == current_user.email).first()
    if not customer or ticket.Customer_CustomerId != customer.CustomerId:
        raise HTTPException(status_code=403, detail="You are not authorized to cancel this ticket")

    result = tickets.cancel_ticket(db, ticket_no)
    if not result:
        raise HTTPException(status_code=400, detail="Cancellation failed")

    return {"message": "Ticket cancelled successfully"}
