# app/routers/admin_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import User as UserSchema
from auth_utils import require_role
import crud.admin as admin_crud

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

@router.get("/users", response_model=list[UserSchema], dependencies=[Depends(require_role("admin"))])
def get_all_users(db: Session = Depends(get_db)):
    return admin_crud.get_all_users(db)

@router.get("/users/{user_id}", response_model=UserSchema, dependencies=[Depends(require_role("admin"))])
def get_user(user_id: int, db: Session = Depends(get_db)):
    return admin_crud.get_user(db, user_id)

@router.put("/users/{user_id}/promote", dependencies=[Depends(require_role("admin"))])
def promote_user(user_id: int, db: Session = Depends(get_db)):
    return admin_crud.promote_user_to_admin(user_id, db)

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_role("admin"))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return admin_crud.delete_user(user_id, db)

# Plays Management
@router.get("/plays", dependencies=[Depends(require_role("admin"))])
def get_all_plays(db: Session = Depends(get_db)):
    return admin_crud.get_all_plays(db)

@router.get("/plays/{play_id}", dependencies=[Depends(require_role("admin"))])
def get_play(play_id: int, db: Session = Depends(get_db)):
    return admin_crud.get_play(db, play_id)

@router.put("/plays/{play_id}", dependencies=[Depends(require_role("admin"))])
def update_play(play_id: int, data: dict, db: Session = Depends(get_db)):
    return admin_crud.update_play(db, play_id, data)

@router.delete("/plays/{play_id}", dependencies=[Depends(require_role("admin"))])
def delete_play(play_id: int, db: Session = Depends(get_db)):
    return admin_crud.delete_play(play_id, db)

# ShowTimes Management
@router.get("/showtimes", dependencies=[Depends(require_role("admin"))])
def get_all_showtimes(db: Session = Depends(get_db)):
    return admin_crud.get_all_showtimes(db)

@router.get("/showtimes/{play_id}/{date_time}", dependencies=[Depends(require_role("admin"))])
def get_showtime(play_id: int, date_time: str, db: Session = Depends(get_db)):
    return admin_crud.get_showtime(db, play_id, date_time)

@router.put("/showtimes/{play_id}/{date_time}", dependencies=[Depends(require_role("admin"))])
def update_showtime(play_id: int, date_time: str, data: dict, db: Session = Depends(get_db)):
    return admin_crud.update_showtime(db, play_id, date_time, data)

@router.delete("/showtimes/{play_id}/{date_time}", dependencies=[Depends(require_role("admin"))])
def delete_showtime(play_id: int, date_time: str, db: Session = Depends(get_db)):
    return admin_crud.delete_showtime(play_id, date_time, db)

# Customers Management
@router.get("/customers", dependencies=[Depends(require_role("admin"))])
def get_all_customers(db: Session = Depends(get_db)):
    return admin_crud.get_all_customers(db)

@router.get("/customers/{customer_id}", dependencies=[Depends(require_role("admin"))])
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return admin_crud.get_customer(db, customer_id)

@router.put("/customers/{customer_id}", dependencies=[Depends(require_role("admin"))])
def update_customer(customer_id: int, data: dict, db: Session = Depends(get_db)):
    return admin_crud.update_customer(db, customer_id, data)

@router.delete("/customers/{customer_id}", dependencies=[Depends(require_role("admin"))])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return admin_crud.delete_customer(customer_id, db)

# Actors Management
@router.get("/actors", dependencies=[Depends(require_role("admin"))])
def get_all_actors(db: Session = Depends(get_db)):
    return admin_crud.get_all_actors(db)

@router.get("/actors/{actor_id}", dependencies=[Depends(require_role("admin"))])
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    return admin_crud.get_actor(db, actor_id)

@router.put("/actors/{actor_id}", dependencies=[Depends(require_role("admin"))])
def update_actor(actor_id: int, data: dict, db: Session = Depends(get_db)):
    return admin_crud.update_actor(db, actor_id, data)

@router.delete("/actors/{actor_id}", dependencies=[Depends(require_role("admin"))])
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    return admin_crud.delete_actor(actor_id, db)

# Directors Management
@router.get("/directors", dependencies=[Depends(require_role("admin"))])
def get_all_directors(db: Session = Depends(get_db)):
    return admin_crud.get_all_directors(db)

@router.get("/directors/{director_id}", dependencies=[Depends(require_role("admin"))])
def get_director(director_id: int, db: Session = Depends(get_db)):
    return admin_crud.get_director(db, director_id)

@router.put("/directors/{director_id}", dependencies=[Depends(require_role("admin"))])
def update_director(director_id: int, data: dict, db: Session = Depends(get_db)):
    return admin_crud.update_director(db, director_id, data)

@router.delete("/directors/{director_id}", dependencies=[Depends(require_role("admin"))])
def delete_director(director_id: int, db: Session = Depends(get_db)):
    return admin_crud.delete_director(director_id, db)

# Tickets Management
@router.get("/tickets", dependencies=[Depends(require_role("admin"))])
def get_all_tickets(db: Session = Depends(get_db)):
    return admin_crud.get_all_tickets(db)

@router.get("/tickets/{ticket_no}", dependencies=[Depends(require_role("admin"))])
def get_ticket(ticket_no: str, db: Session = Depends(get_db)):
    return admin_crud.get_ticket(db, ticket_no)

@router.put("/tickets/{ticket_no}", dependencies=[Depends(require_role("admin"))])
def update_ticket(ticket_no: str, data: dict, db: Session = Depends(get_db)):
    return admin_crud.update_ticket(db, ticket_no, data)

@router.delete("/tickets/{ticket_no}", dependencies=[Depends(require_role("admin"))])
def delete_ticket(ticket_no: str, db: Session = Depends(get_db)):
    return admin_crud.delete_ticket(ticket_no, db)
