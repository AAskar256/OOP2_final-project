from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Actor as ActorModel, ActorPlayAssociation, Play as PlayModel, User
from ..schemas import ActorCreate, Actor as ActorSchema, ActorPlayAssociationCreate
from ..services.auth import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/actors",
    tags=["Actors"]
)

@router.post("/", response_model=ActorSchema, status_code=status.HTTP_201_CREATED)
def create_actor(
    actor: ActorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_actor = ActorModel(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

@router.get("/", response_model=List[ActorSchema])
def read_actors(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search by full name or nationality"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(ActorModel)
    if search:
        query = query.filter(
            (ActorModel.full_name.ilike(f"%{search}%")) | 
            (ActorModel.nationality.ilike(f"%{search}%"))
        )
    actors = query.offset(skip).limit(limit).all()
    return actors

@router.get("/{actor_id}", response_model=ActorSchema)
def read_actor(
    actor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    actor = db.query(ActorModel).filter(ActorModel.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor

@router.put("/{actor_id}", response_model=ActorSchema)
def update_actor(
    actor_id: int,
    actor: ActorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_actor = db.query(ActorModel).filter(ActorModel.id == actor_id).first()
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    
    for key, value in actor.dict().items():
        setattr(db_actor, key, value)

    db.commit()
    db.refresh(db_actor)
    return db_actor

@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_actor(
    actor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    actor = db.query(ActorModel).filter(ActorModel.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    db.delete(actor)
    db.commit()
    return

@router.post("/{actor_id}/plays/{play_id}", response_model=ActorPlayAssociation, status_code=status.HTTP_201_CREATED)
def add_actor_to_play(
    actor_id: int,
    play_id: int,
    association: ActorPlayAssociationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    actor = db.query(ActorModel).filter(ActorModel.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")

    play = db.query(PlayModel).filter(PlayModel.id == play_id).first()
    if play is None:
        raise HTTPException(status_code=404, detail="Play not found")

    db_association = ActorPlayAssociation(
        actor_id=actor_id,
        play_id=play_id,
        role_name=association.role_name
    )
    db.add(db_association)
    db.commit()
    db.refresh(db_association)
    return db_association
