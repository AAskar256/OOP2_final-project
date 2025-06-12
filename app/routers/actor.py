from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Actor, ActorPlayAssociation
from ..schemas import ActorCreate, Actor, ActorPlayAssociationCreate
from ..services.auth import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/actors",
    tags=["actors"]
)

@router.post("/", response_model=Actor)
def create_actor(
    actor: ActorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_actor = Actor(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

@router.get("/", response_model=List[Actor])
def read_actors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    actors = db.query(Actor).offset(skip).limit(limit).all()
    return actors

@router.get("/{actor_id}", response_model=Actor)
def read_actor(
    actor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor

@router.put("/{actor_id}", response_model=Actor)
def update_actor(
    actor_id: int,
    actor: ActorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    for key, value in actor.dict().items():
        setattr(db_actor, key, value)
    db.commit()
    db.refresh(db_actor)
    return db_actor

@router.delete("/{actor_id}")
def delete_actor(
    actor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    db.delete(actor)
    db.commit()
    return {"message": "Actor deleted successfully"}

@router.post("/{actor_id}/plays/{play_id}", response_model=ActorPlayAssociation)
def add_actor_to_play(
    actor_id: int,
    play_id: int,
    association: ActorPlayAssociationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_association = ActorPlayAssociation(
        actor_id=actor_id,
        play_id=play_id,
        role_name=association.role_name
    )
    db.add(db_association)
    db.commit()
    db.refresh(db_association)
    return db_association
