from fastapi import APIRouter, HTTPException
from app.services.inbox_service import get_user_inbox, get_user_outbox

router = APIRouter(prefix="/api")

@router.get("/inboxLetter")
def inbox_letters(user_id: int, character_id: int):  # character_id 파라미터 추가
    inbox_letters = get_user_inbox(user_id, character_id)  # character_id 전달
    if not inbox_letters:
        raise HTTPException(status_code=404, detail="No letters found in the inbox for the specified user ID and character ID")
    return inbox_letters

@router.get("/outboxLetter")
def outbox_letters(user_id: int, character_id: int):
    outbox_letters = get_user_outbox(user_id, character_id)
    if not outbox_letters:
        raise HTTPException(status_code=404, detail="No letters found in the outbox for the specified user ID")
    return outbox_letters
