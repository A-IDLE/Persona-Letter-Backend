from fastapi import APIRouter
from services.letter_service import write_letter
from schemas.schemas import LetterDto

# 여기서 데이터베이스 생성
# models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/writeLetter")
def writeLetter(letter: LetterDto):
    
    letter_sent = letter
    letter_received = write_letter(letter_sent)
    
    return letter_received