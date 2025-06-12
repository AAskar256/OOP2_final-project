from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Ticket, Showtime, User
from ..schemas import TicketCreate, Ticket
from ..utils.auth import get_current_active_user
from ..utils.email import send_ticket_email

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.post("/", response_model=Ticket)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if showtime exists
    showtime = db.query(Showtime).filter(Showtime.id == ticket.showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    
    # Check if seat is available
    existing_ticket = db.query(Ticket).filter(
        Ticket.showtime_id == ticket.showtime_id,
        Ticket.seat_number == ticket.seat_number
    ).first()
    if existing_ticket:
        raise HTTPException(status_code=400, detail="Seat already taken")
    
    # Create ticket
    db_ticket = Ticket(
        **ticket.dict(),
        customer_id=current_user.id,
        booking_time=datetime.utcnow()
    )
    db.add(db_ticket)
    
    # Update available seats
    showtime.available_seats -= 1
    db.commit()
    db.refresh(db_ticket)
    
    # Send email notification
    send_ticket_email(
        email=current_user.email,
        play_title=showtime.play.title,
        showtime_date=showtime.start_time,
        seat_number=ticket.seat_number,
        price=ticket.price
    )
    
    return db_ticket

@router.get("/", response_model=List[Ticket])
def read_tickets(
    skip: int = 0,
    limit: int = 100,
    showtime_id: int = None,
    customer_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Ticket)
    
    if showtime_id:
        query = query.filter(Ticket.showtime_id == showtime_id)
    if customer_id:
        if current_user.role != "admin" and current_user.id != customer_id:
            raise HTTPException(status_code=403, detail="Can only view your own tickets")
        query = query.filter(Ticket.customer_id == customer_id)
    elif current_user.role != "admin":
        query = query.filter(Ticket.customer_id == current_user.id)
    
    tickets = query.offset(skip).limit(limit).all()
    return tickets

@router.get("/{ticket_id}", response_model=Ticket)
def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role != "admin" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only view your own tickets")
    return ticket

@router.put("/{ticket_id}/pay")
def pay_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role != "admin" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only pay for your own tickets")
    if ticket.is_paid:
        raise HTTPException(status_code=400, detail="Ticket already paid")
    
    ticket.is_paid = True
    db.commit()
    return {"message": "Ticket payment successful"}

@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role != "admin" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only delete your own tickets")
    
    # Update available seats
    showtime = db.query(Showtime).filter(Showtime.id == ticket.showtime_id).first()
    if showtime:
        showtime.available_seats += 1
    
    db.delete(ticket)
    db.commit()
    return {"message": "Ticket deleted successfully"}
