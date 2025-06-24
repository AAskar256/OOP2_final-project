from sqlalchemy.orm import Session
from models import Play
from schemas import PlayCreate, PlayUpdate
from fastapi import HTTPException

def create_play(db: Session, play: PlayCreate):
    db_play = Play(**play.dict())
    db.add(db_play)
    db.commit()
    db.refresh(db_play)
    return db_play

def get_play_by_id(db: Session, play_id: int):
    play = db.query(Play).filter(Play.PlayId == play_id).first()
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    return play

def get_all_plays(db: Session):
    return db.query(Play).all()

def update_play(play_id: int, update_data: PlayUpdate, db: Session):
    play = db.query(Play).filter(Play.PlayId == play_id).first()
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(play, key, value)

    db.commit()
    db.refresh(play)
    return play

def delete_play(play_id: int, db: Session):
    play = db.query(Play).filter(Play.PlayId == play_id).first()
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    db.delete(play)
    db.commit()
    return {"detail": "Play deleted successfully"}