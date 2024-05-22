from services.letter_service import write_letter
from schemas.schemas import LetterDto
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from services.letter_service import write_letter
from schemas.schemas import LetterDto
from models.models import Letter
from sqlalchemy.orm import Session
from models.database import get_db
from typing import List
from fastapi import Request
from services.mail.smtp import send_email
from services.letter import get_letters_by_character_id, get_a_letter, get_letters_by_reception_status
from query.letter import update_letter_read_status
from utils.utils import get_user_id_from_request, get_email_from_request


router = APIRouter()


# @router.post("/writeLetter")
# def writeLetter(request: Request, letter: LetterDto):

#     user_info = request.state.user
#     userId = user_info.get("userId")
#     # print(userId)

#     letter_sent = letter
#     letter_received = write_letter(letter_sent)

#     # userEmail을 추출
#     user_info = request.state.user
#     email = user_info.get("email")

#     send_email(email)

#     return letter_received

# # 보낸편지 받은편지 전체 조회
# @router.get("/readLetter")
# def readLetter(db: Session = Depends(get_db)):
#     letters = db.query(Letter).all()
#     return letters

# @router.get("/readLetter/{user_id}/{character_id}")
# def read_letter(user_id: int, character_id: int, db: Session = Depends(get_db)):
#     # 해당 사용자 ID와 캐릭터 ID에 해당하는 편지들을 데이터베이스에서 가져옴
#     letters = db.query(Letter).filter(Letter.user_id == user_id, Letter.character_id == character_id).all()
#     print(letters)
#     return letters


@router.get("/character/{character_id}/letters")
def get_letters(character_id: int, request: Request, db: Session = Depends(get_db)):

    # 사용자의 아이디를 받는다
    user_id = get_user_id_from_request(request)

    letters = get_letters_by_character_id(user_id, character_id, db)

    return letters

# 받은편지 읽음처리
@router.put("/letterStatus/{letter_id}")
def update_letter_status(letter_id: int, db: Session = Depends(get_db)):
    result = update_letter_read_status(letter_id, True)
    if result == "Letter not found.":
        raise HTTPException(status_code=404, detail="Letter not found")
    elif "Error" in result:
        raise HTTPException(status_code=500, detail=result)

    return {"message": result}


@router.get("/letters/{letter_id}")
def get_letter(letter_id: int, request: Request, db: Session = Depends(get_db)):

    # letter_id에 해당하는 편지를 데이터베이스에서 가져옴
    letter = get_a_letter(letter_id, db)

    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")

    # 사용자 Validation
    # 사용자의 아이디를 받는다
    user_id = get_user_id_from_request(request)

    # 편지의 사용자 아이디와 사용자의 아이디가 다르면 401 에러를 발생시킨다
    if (letter.user_id != user_id):
        raise HTTPException(status_code=401, detail="Unauthorized access")

    return letter


@router.post("/letters")
def writeLetter(
    request: Request,
    letter: LetterDto,
    user_id=Depends(get_user_id_from_request)
):

    # 사용자의 아이디를 받는다
    # user_id = get_user_id_from_request(request)

    # letter 초기화
    letter_sent = letter
    letter_sent.user_id = user_id

    letter_received = write_letter(letter_sent)

    # userEmail을 추출
    email = get_email_from_request(request)

    send_email(email)

    return letter_received


@router.get("/character/{characterId}/letters/{receptionStatus}")
def getLettersByCharacterAndReceptionStatus(characterId: int, receptionStatus: str, user_id=Depends(get_user_id_from_request)):
    
    letters = get_letters_by_reception_status(user_id, characterId, receptionStatus)
    
    return letters
    
