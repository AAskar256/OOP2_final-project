from sqlalchemy.orm import Session
from models import BookingAddon
from schemas import BookingAddonCreate, BookingAddonUpdate
from fastapi import HTTPException

def create_addon(db: Session, addon: BookingAddonCreate):
    db_addon = BookingAddon(**addon.dict())
    db.add(db_addon)
    db.commit()
    db.refresh(db_addon)
    return db_addon

def get_addon_by_ticket(db: Session, ticket_no: str):
    return db.query(BookingAddon).filter(BookingAddon.TicketNo == ticket_no).first()

def update_addon(ticket_no: str, update_data: BookingAddonUpdate, db: Session):
    addon = db.query(BookingAddon).filter(BookingAddon.TicketNo == ticket_no).first()
    if not addon:
        raise HTTPException(status_code=404, detail="Addon not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(addon, key, value)

    db.commit()
    db.refresh(addon)
    return addon

def delete_addon(ticket_no: str, db: Session):
    addon = db.query(BookingAddon).filter(BookingAddon.TicketNo == ticket_no).first()
    if not addon:
        raise HTTPException(status_code=404, detail="Addon not found")

    db.delete(addon)
    db.commit()
    return {"detail": "Addon deleted successfully"}