from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import directors
from schemas import Director, DirectorCreate
from database import get_db

router = APIRouter()

@router.post("/", response_model=Director, status_code=status.HTTP_201_CREATED)
def create_director(director: DirectorCreate, db: Session = Depends(get_db)):
    return directors.create_director(db, director)

@router.get("/", response_model=list[Director], status_code=status.HTTP_200_OK)
def get_directors(db: Session = Depends(get_db)):
    return directors.get_directors(db)

@router.get("/{director_id}", response_model=Director, status_code=status.HTTP_200_OK)
def get_director(director_id: int, db: Session = Depends(get_db)):
    director = directors.get_director(db, director_id)
    if director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return director

@router.delete("/{director_id}", status_code=status.HTTP_200_OK)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    return directors.delete_director(db, director_id)


@router.put("/{director_id}", response_model=Director, status_code=status.HTTP_200_OK)
def update_director(director_id: int, director: DirectorCreate, db: Session = Depends(get_db)):
    return directors.update_director(db, director_id, director)
