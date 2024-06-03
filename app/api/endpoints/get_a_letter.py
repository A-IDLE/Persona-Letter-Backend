from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.letter_service import get_a_letter, get_received_letter, get_sent_letter
from app.models.database import get_db

router = APIRouter(prefix="/api")

@router.get("/getALetter/{letter_id}")
def getAletter(letter_id: int):
    letter = get_a_letter(letter_id)
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
    return letter

@router.get("/received")
def receivedLetter(letter_id: int, db: Session = Depends(get_db)):
    letter = get_received_letter(letter_id, db)
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
    return letter

@router.get("/sent")
def receivedLetter(letter_id: int, db: Session = Depends(get_db)):
    letter = get_sent_letter(letter_id, db)
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
    return letter