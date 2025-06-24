
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserCreate, UserLogin, Token
from database import get_db
from crud import auth
from fastapi.security import OAuth2PasswordRequestForm
from auth_utils import create_access_token, authenticate_user

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = auth.create_user(db, user)
    access_token = create_access_token({"sub": new_user.username, "role": new_user.role})
    return {"access_token": access_token, "token_type": "bearer"}




@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}
