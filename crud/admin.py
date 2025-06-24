# app/crud/admin.py
from sqlalchemy.orm import Session
from models import User, Play, ShowTime, Customer, Actor, Director, Ticket
from datetime import datetime

# Users

def get_all_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def promote_user_to_admin(user_id: int, db: Session):
    user = get_user(db, user_id)
    if user:
        user.role = "admin"
        db.commit()
        db.refresh(user)
    return user

def delete_user(user_id: int, db: Session):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user

# Plays

def get_all_plays(db: Session):
    return db.query(Play).all()

def get_play(db: Session, play_id: int):
    return db.query(Play).filter(Play.PlayId == play_id).first()

def update_play(db: Session, play_id: int, data: dict):
    play = get_play(db, play_id)
    if play:
        for key, value in data.items():
            setattr(play, key, value)
        db.commit()
        db.refresh(play)
    return play

def delete_play(play_id: int, db: Session):
    play = get_play(db, play_id)
    if play:
        db.delete(play)
        db.commit()
    return play

# ShowTimes

def get_all_showtimes(db: Session):
    return db.query(ShowTime).all()

def get_showtime(db: Session, play_id: int, date_time: str):
    dt = datetime.fromisoformat(date_time)
    return db.query(ShowTime).filter(ShowTime.Play_PlayId == play_id, ShowTime.DateAndTime == dt).first()

def update_showtime(db: Session, play_id: int, date_time: str, data: dict):
    showtime = get_showtime(db, play_id, date_time)
    if showtime:
        for key, value in data.items():
            setattr(showtime, key, value)
        db.commit()
        db.refresh(showtime)
    return showtime

def delete_showtime(play_id: int, date_time: str, db: Session):
    showtime = get_showtime(db, play_id, date_time)
    if showtime:
        db.delete(showtime)
        db.commit()
    return showtime

# Customers

def get_all_customers(db: Session):
    return db.query(Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.CustomerId == customer_id).first()

def update_customer(db: Session, customer_id: int, data: dict):
    customer = get_customer(db, customer_id)
    if customer:
        for key, value in data.items():
            setattr(customer, key, value)
        db.commit()
        db.refresh(customer)
    return customer

def delete_customer(customer_id: int, db: Session):
    customer = get_customer(db, customer_id)
    if customer:
        db.delete(customer)
        db.commit()
    return customer

# Actors

def get_all_actors(db: Session):
    return db.query(Actor).all()

def get_actor(db: Session, actor_id: int):
    return db.query(Actor).filter(Actor.ActorId == actor_id).first()

def update_actor(db: Session, actor_id: int, data: dict):
    actor = get_actor(db, actor_id)
    if actor:
        for key, value in data.items():
            setattr(actor, key, value)
        db.commit()
        db.refresh(actor)
    return actor

def delete_actor(actor_id: int, db: Session):
    actor = get_actor(db, actor_id)
    if actor:
        db.delete(actor)
        db.commit()
    return actor

# Directors

def get_all_directors(db: Session):
    return db.query(Director).all()

def get_director(db: Session, director_id: int):
    return db.query(Director).filter(Director.DirectorId == director_id).first()

def update_director(db: Session, director_id: int, data: dict):
    director = get_director(db, director_id)
    if director:
        for key, value in data.items():
            setattr(director, key, value)
        db.commit()
        db.refresh(director)
    return director

def delete_director(director_id: int, db: Session):
    director = get_director(db, director_id)
    if director:
        db.delete(director)
        db.commit()
    return director

# Tickets

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def get_ticket(db: Session, ticket_no: str):
    return db.query(Ticket).filter(Ticket.TicketNo == ticket_no).first()

def update_ticket(db: Session, ticket_no: str, data: dict):
    ticket = get_ticket(db, ticket_no)
    if ticket:
        for key, value in data.items():
            setattr(ticket, key, value)
        db.commit()
        db.refresh(ticket)
    return ticket

def delete_ticket(ticket_no: str, db: Session):
    ticket = get_ticket(db, ticket_no)
    if ticket:
        db.delete(ticket)
        db.commit()
    return ticket
