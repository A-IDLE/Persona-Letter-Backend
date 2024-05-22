from fastapi import APIRouter
from services.character_service import get_characters
from schemas.schemas import CharacterDto
from fastapi import FastAPI,APIRouter, Depends, Request
from services.letter_service import write_letter
from schemas.schemas import CharacterDto
from models.models import Character
from sqlalchemy.orm import Session
from models.database import get_db
from typing import List
from fastapi import Request
from services.mail.smtp import send_email
from fastapi import HTTPException

router = APIRouter()

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