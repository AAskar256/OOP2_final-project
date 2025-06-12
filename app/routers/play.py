
@router.get("/search/", response_model=List[Play])
def search_plays(
    title: str = None,
    genre: str = None,
    director_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Play)
    
    if title:
        query = query.filter(Play.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(Play.genre.ilike(f"%{genre}%"))
    if director_id:
        query = query.filter(Play.director_id == director_id)
    
    plays = query.offset(skip).limit(limit).all()
    return plays
