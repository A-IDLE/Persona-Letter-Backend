from services.letter_service import write_letter
from schemas.schemas import LetterDto
from fastapi import FastAPI,APIRouter, Depends, Request
from services.letter_service import write_letter
from schemas.schemas import LetterDto
from models.models import Letter
from sqlalchemy.orm import Session
from models.database import get_db
from typing import List
from fastapi import Request
from services.mail.smtp import send_email


router = APIRouter()

@router.post("/writeLetter")
def writeLetter(request: Request, letter: LetterDto):

    user_info = request.state.user
    userId = user_info.get("userId")
    # print(userId)

    
    letter_sent = letter
    letter_received = write_letter(letter_sent)
    
    # userEmail을 추출
    user_info = request.state.user
    email = user_info.get("email")
    
    send_email(email)
    
    return letter_received

# 보낸편지 받은편지 전체 조회
@router.get("/readLetter")
def readLetter(db: Session = Depends(get_db)):
    letters = db.query(Letter).all()
    return letters

@router.get("/readLetter/{user_id}/{character_id}")
def read_letter(user_id: int, character_id: int, db: Session = Depends(get_db)):
    # 해당 사용자 ID와 캐릭터 ID에 해당하는 편지들을 데이터베이스에서 가져옴
    letters = db.query(Letter).filter(Letter.user_id == user_id, Letter.character_id == character_id).all()
    print(letters)
    return letters



# @router.get("/test")
# def test(request: Request):
#     user_info = request.state.user
#     email = user_info.get("email")
#     print(email)
#     return {"email": email}