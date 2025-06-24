from datetime import datetime
from sqlalchemy.orm import Session
import models
from models import ShowTime
from schemas import ShowTimeCreate

# create
def create_showtime(db: Session, showtime: ShowTimeCreate):
    db_showtime = ShowTime(**showtime.dict())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

# read
def get_showtimes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ShowTime).offset(skip).limit(limit).all()

def get_upcoming_showtimes(db: Session, now: datetime | None = None):
    now = now or datetime.utcnow()
    return (
        db.query(ShowTime)
        .filter(ShowTime.DateAndTime >= now)
        .order_by(ShowTime.DateAndTime)
        .all()
    )

def get_showtimes_by_play(db: Session, play_id: int):
    return (
        db.query(ShowTime)
        .filter(ShowTime.Play_PlayId == play_id)
        .order_by(ShowTime.DateAndTime)
        .all()
    )

# ── update
def update_showtime(db: Session, play_id: int, date_time: str, updated: ShowTimeCreate):
    dt = datetime.fromisoformat(date_time)
    showtime = (
        db.query(ShowTime)
        .filter(
            ShowTime.Play_PlayId == play_id,
            ShowTime.DateAndTime == dt
        )
        .first()
    )
    if showtime:
        for key, value in updated.dict().items():
            setattr(showtime, key, value)
        db.commit()
        db.refresh(showtime)
    return showtime

#  delete
def delete_showtime(db: Session, play_id: int, date_time: str):
    dt = datetime.fromisoformat(date_time)
    showtime = (
        db.query(ShowTime)
        .filter(
            ShowTime.Play_PlayId == play_id,
            ShowTime.DateAndTime == dt
        )
        .first()
    )
    if showtime:
        db.delete(showtime)
        db.commit()
    return showtime
