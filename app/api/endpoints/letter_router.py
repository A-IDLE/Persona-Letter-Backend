from services.letter_service import write_letter
from schemas.schemas import LetterDto
from fastapi import FastAPI,APIRouter, Depends, Request
from services.letter_service import write_letter
from schemas.schemas import LetterDto
from models.models import Letter
from sqlalchemy.orm import Session
from models.database import get_db
from typing import List


router = APIRouter()

@router.post("/writeLetter")
def writeLetter(request: Request, letter: LetterDto):
    user_info = request.state.user
    userId = user_info.get("userId")
    print(userId)
    
    letter_sent = letter
    letter_received = write_letter(letter_sent)
    
    return letter_received

# 보낸편지 받은편지 전체 조회
@router.get("/readLetter", response_model=List[LetterDto])
def readLetter(db: Session = Depends(get_db)):
    letters = db.query(Letter).all()
    return letters

@router.get("/readLetter/{user_id}", response_model=List[LetterDto])
def read_letter(user_id: int, db: Session = Depends(get_db)):
    # 해당 사용자 ID에 해당하는 편지들을 데이터베이스에서 가져옴
    letters = db.query(Letter).filter(Letter.user_id == user_id).all()
    return letters


# @router.get("/test")
# def test(request: Request):
#     user_info = request.state.user
#     email = user_info.get("email")
#     print(email)
#     return {"email": email}