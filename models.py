# models.py
# ───────────────────────────────────────
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# users

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")




# plays
class Play(Base):
    __tablename__ = "plays"
    PlayId = Column(Integer, primary_key=True, index=True)
    Title = Column(String)
    Duration = Column(Integer)
    Genre = Column(String)
    Synopsis = Column(String)

# customers
class Customer(Base):
    __tablename__ = "customers"
    CustomerId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    TelephoneNo = Column(String)

# actors
class Actor(Base):
    __tablename__ = "actors"
    ActorId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Gender = Column(String)
    Play_PlayId = Column(Integer, ForeignKey("plays.PlayId"))

# directors
class Director(Base):
    __tablename__ = "directors"
    DirectorId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Gender = Column(String)
    Play_PlayId = Column(Integer, ForeignKey("plays.PlayId"))

# showtimes
class ShowTime(Base):
    __tablename__ = "showtimes"
    DateAndTime = Column(DateTime, primary_key=True)
    Play_PlayId = Column(Integer, ForeignKey("plays.PlayId"), primary_key=True)

# tickets
class Ticket(Base):
    __tablename__ = "tickets"
    TicketNo = Column(String, primary_key=True)
    Seat_RowNo = Column(Integer)
    Seat_SeatNo = Column(Integer)
    ShowTime_DateAndTime = Column(DateTime)
    ShowTime_Play_PlayId = Column(Integer)
    Customer_CustomerId = Column(Integer, ForeignKey("customers.CustomerId"))

# booking-addons
class BookingAddon(Base):
    __tablename__ = "bookingaddons"
    TicketNo = Column(String, ForeignKey("tickets.TicketNo"), primary_key=True)
    food = Column(String)
    drinks = Column(String)
    flowers = Column(Boolean)

# payments
class Payment(Base):
    __tablename__ = "payments"
    TicketNo = Column(String, ForeignKey("tickets.TicketNo"), primary_key=True)
    amount = Column(Float)
    payment_method = Column(String)
    status = Column(String)
    receipt_no = Column(String, unique=True)
