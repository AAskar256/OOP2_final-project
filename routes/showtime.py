from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import showtimes
from schemas import ShowTime, ShowTimeCreate
from database import get_db
from auth_utils import require_role
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=ShowTime, status_code=status.HTTP_201_CREATED)
def create_showtime(
    showtime: ShowTimeCreate,
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin"))
):
    return showtimes.create_showtime(db, showtime)

@router.get("/", response_model=list[ShowTime], status_code=status.HTTP_200_OK)
def get_showtimes(db: Session = Depends(get_db)):
    return showtimes.get_showtimes(db)

@router.get("/upcoming", response_model=list[ShowTime])
def get_upcoming_showtimes(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    return showtimes.get_upcoming_showtimes(db, now)

@router.get("/by_play/{play_id}", response_model=list[ShowTime])
def get_showtimes_by_play(play_id: int, db: Session = Depends(get_db)):
    return showtimes.get_showtimes_by_play(db, play_id)

@router.put("/{play_id}/{date_time}", response_model=ShowTime)
def update_showtime(
    play_id: int,
    date_time: str,
    showtime: ShowTimeCreate,
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin"))
):
    updated = showtimes.update_showtime(db, play_id, date_time, showtime)
    if not updated:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return updated

@router.delete("/{play_id}/{date_time}", status_code=status.HTTP_200_OK)
def delete_showtime(
    play_id: int,
    date_time: str,
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin"))
):
    deleted = showtimes.delete_showtime(db, play_id, date_time)
    if not deleted:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return {"detail": "Showtime deleted"}
