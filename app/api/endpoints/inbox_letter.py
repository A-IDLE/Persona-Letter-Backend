from fastapi import APIRouter, HTTPException
from services.inbox_service import get_user_inbox

router = APIRouter()

@router.get("/inboxLetter")
def inbox_letters(user_id: int):
    letters = get_user_inbox(user_id)  # 사용자 ID로 받은 편지함 조회 함수 호출
    if not letters:
        raise HTTPException(status_code=404, detail="No letters found for the specified user ID")
    return letters