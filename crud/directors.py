from sqlalchemy.orm import Session
from models import Director
from schemas import DirectorCreate

def create_director(db: Session, director: DirectorCreate):
    db_director = Director(**director.dict())
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

def get_directors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Director).offset(skip).limit(limit).all()

def get_director(db: Session, director_id: int):
    return db.query(Director).filter(Director.DirectorId == director_id).first()

def delete_director(db: Session, director_id: int):
    director = db.query(Director).filter(Director.DirectorId == director_id).first()
    if director:
        db.delete(director)
        db.commit()
    return director

def update_director(db: Session, director_id: int, updated: DirectorCreate):
    director = db.query(Director).filter(Director.DirectorId == director_id).first()
    if director:
        for key, value in updated.dict().items():
            setattr(director, key, value)
        db.commit()
        db.refresh(director)
    return director
