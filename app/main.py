from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    actor, 
    auth, 
    customer, 
    director, 
    play, 
    showtime, 
    ticket
)
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sierra Leone Concert Association API",
    description="API for managing concert database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(actor.router)
app.include_router(director.router)
app.include_router(play.router)
app.include_router(showtime.router)
app.include_router(ticket.router)
app.include_router(customer.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Sierra Leone Concert Association API"}
