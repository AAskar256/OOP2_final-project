from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Director
from ..schemas import DirectorCreate, Director
from ..utils.auth import get_current_active_user

router = APIRouter(
    prefix="/directors",
    tags=["directors"]
)

@router.post("/", response_model=Director)
def create_director(
    director: DirectorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create directors")
    db_director = Director(**director.dict())
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

@router.get("/", response_model=List[Director])
def read_directors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    directors = db.query(Director).offset(skip).limit(limit).all()
    return directors

@router.get("/{director_id}", response_model=Director)
def read_director(
    director_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    director = db.query(Director).filter(Director.id == director_id).first()
    if director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return director

@router.put("/{director_id}", response_model=Director)
def update_director(
    director_id: int,
    director: DirectorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update directors")
    db_director = db.query(Director).filter(Director.id == director_id).first()
    if db_director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    for key, value in director.dict().items():
        setattr(db_director, key, value)
    db.commit()
    db.refresh(db_director)
    return db_director

@router.delete("/{director_id}")
def delete_director(
    director_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete directors")
    director = db.query(Director).filter(Director.id == director_id).first()
    if director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    db.delete(director)
    db.commit()
    return {"message": "Director deleted successfully"}
