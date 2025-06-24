from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import actors
from schemas import Actor, ActorCreate
from database import get_db
from auth_utils import require_role   # only needed for write ops

router = APIRouter()

# ── write operations ────────────────────────────────────────────
@router.post("/", response_model=Actor, status_code=status.HTTP_201_CREATED)
def create_actor(
    actor: ActorCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin"))
):
    return actors.create_actor(db, actor)

@router.put("/{actor_id}", response_model=Actor)
def update_actor(
    actor_id: int,
    actor: ActorCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin"))
):
    return actors.update_actor(db, actor_id, actor)

@router.delete("/{actor_id}", status_code=status.HTTP_200_OK)
def delete_actor(
    actor_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin"))
):
    return actors.delete_actor(db, actor_id)

# ── read operations (open to all) ────────────────────────────────
@router.get("/", response_model=list[Actor], status_code=status.HTTP_200_OK)
def get_actors(db: Session = Depends(get_db)):
    return actors.get_actors(db)

@router.get("/{actor_id}", response_model=Actor, status_code=status.HTTP_200_OK)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = actors.get_actor(db, actor_id)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor
