from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.database import get_db
from app.models.models import Character
from app.services.character_service import get_characters

router = APIRouter(prefix="/api")

@router.get("/characters")
def getCharacters():

    characters = get_characters()
    
    return characters

@router.get("/character/{character_id}/name")
def get_character_name(character_id: int, db: Session = Depends(get_db)):
    charName = db.query(Character).filter(Character.character_id == character_id).first()
    if not charName:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"name": charName.character_name}