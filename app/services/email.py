from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from .config import settings
from datetime import datetime

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

async def send_ticket_email(
    email: str,
    play_title: str,
    showtime_date: datetime,
    seat_number: str,
    price: float
):
    message = MessageSchema(
        subject="Your Concert Ticket Confirmation",
        recipients=[email],
        body=f"""
        Thank you for booking with Sierra Leone Concert Association!
        
        Play: {play_title}
        Date: {showtime_date.strftime("%Y-%m-%d %H:%M")}
        Seat: {seat_number}
        Price: ${price:.2f}
        
        Enjoy the show!
        """,
        subtype="plain"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)

def send_ticket_email_background(
    background_tasks: BackgroundTasks,
    email: str,
    play_title: str,
    showtime_date: datetime,
    seat_number: str,
    price: float
):
    background_tasks.add_task(
        send_ticket_email,
        email,
        play_title,
        showtime_date,
        seat_number,
        price
    )
