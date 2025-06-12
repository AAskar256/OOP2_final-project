from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="customer")

    tickets = relationship("Ticket", back_populates="customer")

class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    genre = Column(String)
    duration_minutes = Column(Integer)
    director_id = Column(Integer, ForeignKey("directors.id"))

    director = relationship("Director", back_populates="plays")
    showtimes = relationship("Showtime", back_populates="play")
    actors = relationship("ActorPlayAssociation", back_populates="play")

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    bio = Column(String)
    nationality = Column(String)

    plays = relationship("ActorPlayAssociation", back_populates="actor")

class ActorPlayAssociation(Base):
    __tablename__ = "actor_play_association"

    actor_id = Column(Integer, ForeignKey("actors.id"), primary_key=True)
    play_id = Column(Integer, ForeignKey("plays.id"), primary_key=True)
    role_name = Column(String)

    actor = relationship("Actor", back_populates="plays")
    play = relationship("Play", back_populates="actors")

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    bio = Column(String)
    nationality = Column(String)

    plays = relationship("Play", back_populates="director")

class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)
    play_id = Column(Integer, ForeignKey("plays.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    venue = Column(String)
    available_seats = Column(Integer)

    play = relationship("Play", back_populates="showtimes")
    tickets = relationship("Ticket", back_populates="showtime")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    customer_id = Column(Integer, ForeignKey("users.id"))
    seat_number = Column(String)
    price = Column(Float)
    booking_time = Column(DateTime)
    is_paid = Column(Boolean, default=False)

    showtime = relationship("Showtime", back_populates="tickets")
    customer = relationship("User", back_populates="tickets")
