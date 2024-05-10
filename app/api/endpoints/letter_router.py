from services.letter_service import write_letter
from schemas.schemas import LetterDto
from fastapi import FastAPI,APIRouter, Depends
from services.letter_service import write_letter
from schemas.schemas import LetterDto
from models.models import Letter
from sqlalchemy.orm import Session
from models.database import get_db
from typing import List


router = APIRouter()

@router.post("/writeLetter")
def writeLetter(letter: LetterDto):
    
    letter_sent = letter
    letter_received = write_letter(letter_sent)
    
    return letter_received

# 보낸편지 받은편지 전체 조회
@router.get("/readLetter", response_model=List[LetterDto])
def readLetter(db: Session = Depends(get_db)):
    letters = db.query(Letter).all()
    return letters