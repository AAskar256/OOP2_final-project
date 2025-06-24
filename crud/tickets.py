from sqlalchemy.orm import Session
from models import Ticket, ShowTime
from schemas import TicketCreate
from fastapi import HTTPException, status
from datetime import datetime, timedelta

def create_ticket(db: Session, ticket: TicketCreate):
    # Check if seat is already booked for this showtime
    existing = db.query(Ticket).filter(
        Ticket.Seat_RowNo == ticket.Seat_RowNo,
        Ticket.Seat_SeatNo == ticket.Seat_SeatNo,
        Ticket.ShowTime_DateAndTime == ticket.ShowTime_DateAndTime,
        Ticket.ShowTime_Play_PlayId == ticket.ShowTime_Play_PlayId
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Seat already booked for this showtime.")

    db_ticket = Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_no: str):
    ticket = db.query(Ticket).filter(Ticket.TicketNo == ticket_no).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

def delete_ticket(db: Session, ticket_no: str):
    ticket = db.query(Ticket).filter(Ticket.TicketNo == ticket_no).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    showtime = db.query(ShowTime).filter(
        ShowTime.DateAndTime == ticket.ShowTime_DateAndTime,
        ShowTime.Play_PlayId == ticket.ShowTime_Play_PlayId
    ).first()

    if not showtime:
        raise HTTPException(status_code=404, detail="Associated showtime not found")

    if showtime.DateAndTime - datetime.utcnow() < timedelta(hours=3):
        raise HTTPException(status_code=403, detail="Ticket can only be canceled 3+ hours before the showtime")

    db.delete(ticket)
    db.commit()
    return {"detail": "Ticket successfully canceled"}

def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def get_ticket_by_number(db: Session, ticket_no: str):
    return db.query(Ticket).filter(Ticket.TicketNo == ticket_no).first()

