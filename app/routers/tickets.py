from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional
from ..database import get_db
from ..models import Ticket as TicketModel, Showtime, User
from ..schemas import TicketCreate, Ticket as TicketSchema
from ..utils.auth import get_current_active_user, get_current_admin_user
from ..utils.email import send_ticket_email

router = APIRouter(prefix="/tickets", tags=["Tickets"])

TICKET_EXPIRATION_MINUTES = 15

@router.post("/", response_model=TicketSchema)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    showtime = db.query(Showtime).filter(Showtime.id == ticket.showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    existing_ticket = db.query(TicketModel).filter(
        TicketModel.showtime_id == ticket.showtime_id,
        TicketModel.seat_number == ticket.seat_number
    ).first()
    if existing_ticket:
        raise HTTPException(status_code=400, detail="Seat already taken")

    db_ticket = TicketModel(
        **ticket.dict(),
        customer_id=current_user.id,
        booking_time=datetime.utcnow()
    )
    db.add(db_ticket)
    showtime.available_seats -= 1
    db.commit()
    db.refresh(db_ticket)

    send_ticket_email(
        email=current_user.email,
        play_title=showtime.play.title,
        showtime_date=showtime.start_time,
        seat_number=ticket.seat_number,
        price=ticket.price
    )
    return db_ticket

@router.get("/", response_model=List[TicketSchema])
def read_tickets(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = Query("booking_time", regex="^(booking_time)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(TicketModel)
    if current_user.role != "admin":
        query = query.filter(TicketModel.customer_id == current_user.id)

    sort_column = getattr(TicketModel, sort_by)
    if sort_order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    return query.order_by(sort_column).offset(skip).limit(limit).all()

@router.get("/my-tickets", response_model=List[TicketSchema])
def my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(TicketModel).filter(TicketModel.customer_id == current_user.id).all()

@router.get("/{ticket_id}", response_model=TicketSchema)
def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role != "admin" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access to this ticket")
    return ticket

@router.put("/{ticket_id}/pay")
def pay_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role != "admin" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
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
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role != "admin" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    showtime = db.query(Showtime).filter(Showtime.id == ticket.showtime_id).first()
    if showtime:
        showtime.available_seats += 1

    db.delete(ticket)
    db.commit()
    return {"message": "Ticket deleted successfully"}

@router.put("/{ticket_id}/refund")
def refund_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role != "admin" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if not ticket.is_paid:
        raise HTTPException(status_code=400, detail="Cannot refund unpaid ticket")

    ticket.is_paid = False
    showtime = db.query(Showtime).filter(Showtime.id == ticket.showtime_id).first()
    if showtime:
        showtime.available_seats += 1

    db.commit()
    return {"message": "Ticket refunded successfully"}

@router.get("/showtimes/{showtime_id}/available-seats")
def available_seats(
    showtime_id: int,
    db: Session = Depends(get_db)
):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    all_seats = {f"A{i}" for i in range(1, showtime.available_seats + 101)}  # Customize
    taken_seats = {
        ticket.seat_number
        for ticket in db.query(TicketModel).filter(TicketModel.showtime_id == showtime_id).all()
    }
    available = sorted(list(all_seats - taken_seats))
    return {"available_seats": available, "total_available": showtime.available_seats}

@router.delete("/cleanup-unpaid")
def cleanup_unpaid_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    expiration_time = datetime.utcnow() - timedelta(minutes=TICKET_EXPIRATION_MINUTES)
    unpaid_tickets = db.query(TicketModel).filter(
        TicketModel.is_paid == False,
        TicketModel.booking_time < expiration_time
    ).all()

    count = len(unpaid_tickets)
    for ticket in unpaid_tickets:
        showtime = db.query(Showtime).filter(Showtime.id == ticket.showtime_id).first()
        if showtime:
            showtime.available_seats += 1
        db.delete(ticket)
    db.commit()
    return {"message": f"Deleted {count} expired unpaid tickets"}

@router.get("/report")
def sales_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    sales = db.query(
        Showtime.id,
        Showtime.venue,
        Showtime.start_time,
        func.count(TicketModel.id).label("tickets_sold"),
        func.sum(TicketModel.price).label("total_revenue")
    ).join(TicketModel, Showtime.id == TicketModel.showtime_id).group_by(Showtime.id).all()

    return [{"showtime_id": s.id, "venue": s.venue, "start_time": s.start_time, "tickets_sold": s.tickets_sold, "total_revenue": s.total_revenue or 0} for s in sales]
