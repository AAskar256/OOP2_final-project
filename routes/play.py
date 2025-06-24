from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import Play, PlayCreate, PlayUpdate
from crud import plays

router = APIRouter()

@router.post("/", response_model=Play, status_code=status.HTTP_201_CREATED)
def create_play(play: PlayCreate, db: Session = Depends(get_db)):
    return plays.create_play(db, play)

@router.get("/", response_model=list[Play])
def get_all_plays(db: Session = Depends(get_db)):
    return plays.get_all_plays(db)

@router.get("/{play_id}", response_model=Play)
def get_play(play_id: int, db: Session = Depends(get_db)):
    play = plays.get_play_by_id(db, play_id)
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    return play

@router.put("/{play_id}", response_model=Play)
def update_play(play_id: int, update: PlayUpdate, db: Session = Depends(get_db)):
    play = plays.update_play(play_id, update, db)
    if not play:
        raise HTTPException(status_code=404, detail="Play not found or update failed")
    return play

@router.delete("/{play_id}", status_code=status.HTTP_200_OK)
def delete_play(play_id: int, db: Session = Depends(get_db)):
    result = plays.delete_play(play_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Play not found or delete failed")
    return {"message": "Play deleted successfully"}