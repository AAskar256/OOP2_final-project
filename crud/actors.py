from sqlalchemy.orm import Session
from models import Actor
from schemas import ActorCreate

def create_actor(db: Session, actor: ActorCreate):
    db_actor = Actor(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

def get_actors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Actor).offset(skip).limit(limit).all()

def get_actor(db: Session, actor_id: int):
    return db.query(Actor).filter(Actor.ActorId == actor_id).first()

def delete_actor(db: Session, actor_id: int):
    actor = db.query(Actor).filter(Actor.ActorId == actor_id).first()
    if actor:
        db.delete(actor)
        db.commit()
    return actor

def update_actor(db: Session, actor_id: int, updated: ActorCreate):
    actor = db.query(Actor).filter(Actor.ActorId == actor_id).first()
    if actor:
        for key, value in updated.dict().items():
            setattr(actor, key, value)
        db.commit()
        db.refresh(actor)
    return actor
