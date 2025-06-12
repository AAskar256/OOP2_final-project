from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import Showtime
from ..schemas import ShowtimeCreate, Showtime
from ..utils.auth import get_current_active_user

router = APIRouter(
    prefix="/showtimes",
    tags=["showtimes"]
)

@router.post("/", response_model=Showtime)
def create_showtime(
    showtime: ShowtimeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create showtimes")
    db_showtime = Showtime(**showtime.dict())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

@router.get("/", response_model=List[Showtime])
def read_showtimes(
    skip: int = 0,
    limit: int = 100,
    play_id: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Showtime)
    
    if play_id:
        query = query.filter(Showtime.play_id == play_id)
    if start_date:
        query = query.filter(Showtime.start_time >= start_date)
    if end_date:
        query = query.filter(Showtime.end_time <= end_date)
    
    showtimes = query.offset(skip).limit(limit).all()
    return showtimes

@router.get("/{showtime_id}", response_model=Showtime)
def read_showtime(
    showtime_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if showtime is None:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return showtime

@router.put("/{showtime_id}", response_model=Showtime)
def update_showtime(
    showtime_id: int,
    showtime: ShowtimeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update showtimes")
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if db_showtime is None:
        raise HTTPException(status_code=404, detail="Showtime not found")
    for key, value in showtime.dict().items():
        setattr(db_showtime, key, value)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

@router.delete("/{showtime_id}")
def delete_showtime(
    showtime_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete showtimes")
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if showtime is None:
        raise HTTPException(status_code=404, detail="Showtime not found")
    db.delete(showtime)
    db.commit()
    return {"message": "Showtime deleted successfully"}
