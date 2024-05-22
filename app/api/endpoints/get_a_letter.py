from fastapi import APIRouter, HTTPException
from app.services.letter_service import get_a_letter

router = APIRouter()

@router.get("/getALetter/{letter_id}")
def getAletter(letter_id: int):
    letter = get_a_letter(letter_id)
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
    return letter