from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import BookingAddon, BookingAddonCreate, BookingAddonUpdate
from crud import addons

router = APIRouter()

@router.post("/", response_model=BookingAddon, status_code=status.HTTP_201_CREATED)
def create_addon(addon: BookingAddonCreate, db: Session = Depends(get_db)):
    return addons.create_addon(db, addon)

@router.get("/{ticket_no}", response_model=BookingAddon)
def get_addon(ticket_no: str, db: Session = Depends(get_db)):
    addon = addons.get_addon_by_ticket(db, ticket_no)
    if not addon:
        raise HTTPException(status_code=404, detail="Addon not found")
    return addon

@router.put("/{ticket_no}", response_model=BookingAddon)
def update_addon(ticket_no: str, update: BookingAddonUpdate, db: Session = Depends(get_db)):
    return addons.update_addon(ticket_no, update, db)

@router.delete("/{ticket_no}", status_code=status.HTTP_200_OK)
def delete_addon(ticket_no: str, db: Session = Depends(get_db)):
    return addons.delete_addon(ticket_no, db)