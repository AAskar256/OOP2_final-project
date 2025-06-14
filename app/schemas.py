from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    role: str

    class Config:
        orm_mode = True


class DirectorBase(BaseModel):
    full_name: str
    bio: str
    nationality: str

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int

    class Config:
        orm_mode = True


class ActorBase(BaseModel):
    full_name: str
    bio: str
    nationality: str

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int

    class Config:
        orm_mode = True


class PlayBase(BaseModel):
    title: str
    description: str
    genre: str
    duration_minutes: int

class PlayCreate(PlayBase):
    director_id: int

class Play(PlayBase):
    id: int
    director: Optional[Director]  # Nested director

    class Config:
        orm_mode = True


class ShowtimeBase(BaseModel):
    start_time: datetime
    end_time: datetime
    venue: str
    available_seats: int

class ShowtimeCreate(ShowtimeBase):
    play_id: int

class Showtime(ShowtimeBase):
    id: int
    play: Play  # Nested play

    class Config:
        orm_mode = True


class TicketBase(BaseModel):
    seat_number: str
    price: float

class TicketCreate(TicketBase):
    showtime_id: int
    customer_id: Optional[int]  # Might come from authenticated user

class Ticket(TicketBase):
    id: int
    showtime: Showtime
    customer: User
    booking_time: datetime
    is_paid: bool

    class Config:
        orm_mode = True


class ActorPlayAssociationBase(BaseModel):
    role_name: str

class ActorPlayAssociationCreate(ActorPlayAssociationBase):
    actor_id: int
    play_id: int

class ActorPlayAssociation(ActorPlayAssociationBase):
    actor: Actor
    play: Play

    class Config:
        orm_mode = True
