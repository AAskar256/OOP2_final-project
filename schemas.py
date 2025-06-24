from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# Play
class PlayBase(BaseModel):
    Title: str
    Duration: int
    Genre: str
    Synopsis: str

class PlayCreate(PlayBase):
    pass

class PlayUpdate(PlayBase):
    pass

class Play(PlayBase):
    PlayId: int

    class Config:
        orm_mode = True

# Customer
class CustomerBase(BaseModel):
    Name: str
    TelephoneNo: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    CustomerId: int

    class Config:
        orm_mode = True

# Actor
class ActorBase(BaseModel):
    Name: str
    Gender: str
    Play_PlayId: int

class ActorCreate(ActorBase):
    pass

class ActorUpdate(ActorBase):
    pass

class Actor(ActorBase):
    ActorId: int

    class Config:
        orm_mode = True

# Director
class DirectorBase(BaseModel):
    Name: str
    Gender: str
    Play_PlayId: int

class DirectorCreate(DirectorBase):
    pass

class DirectorUpdate(DirectorBase):
    pass

class Director(DirectorBase):
    DirectorId: int

    class Config:
        orm_mode = True

# ShowTime
class ShowTimeBase(BaseModel):
    DateAndTime: datetime
    Play_PlayId: int

class ShowTimeCreate(ShowTimeBase):
    pass

class ShowTimeUpdate(ShowTimeBase):
    pass

class ShowTime(ShowTimeBase):
    class Config:
        orm_mode = True

# Ticket
class TicketBase(BaseModel):
    TicketNo: str
    Seat_RowNo: int
    Seat_SeatNo: int
    ShowTime_DateAndTime: datetime
    ShowTime_Play_PlayId: int
    Customer_CustomerId: int

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    class Config:
        orm_mode = True

# BookingAddon
class BookingAddonBase(BaseModel):
    TicketNo: str
    food: Optional[str]
    drinks: Optional[str]
    flowers: Optional[bool] = False

class BookingAddonCreate(BookingAddonBase):
    pass

class BookingAddonUpdate(BaseModel):
    food: Optional[str]
    drinks: Optional[str]
    flowers: Optional[bool]

class BookingAddon(BookingAddonBase):
    class Config:
        orm_mode = True

# Payment
class PaymentBase(BaseModel):
    TicketNo: str
    amount: float
    payment_method: str
    status: str
    receipt_no: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    class Config:
        orm_mode = True
