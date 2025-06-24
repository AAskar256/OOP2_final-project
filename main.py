from fastapi import FastAPI
from database import Base, engine
from models import *

from routes import (
    auth, play, ticket, addon, payment,
    actor, director, customer, showtime
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sierra Leone Concert Association API")

# Route registration
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(play.router, prefix="/plays", tags=["Plays"])
app.include_router(ticket.router, prefix="/tickets", tags=["Tickets"])
app.include_router(addon.router, prefix="/addons", tags=["Special Booking Addons"])
app.include_router(payment.router, prefix="/payments", tags=["Payments"])
app.include_router(actor.router, prefix="/actors", tags=["Actors"])
app.include_router(director.router, prefix="/directors", tags=["Directors"])
app.include_router(customer.router, prefix="/customers", tags=["Customers"])
app.include_router(showtime.router, prefix="/showtimes", tags=["Showtimes"])

@app.get("/")
def home():
    return {"message": "Welcome to the Sierra Leone Concert Association API"}