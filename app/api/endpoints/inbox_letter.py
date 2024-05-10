from fastapi import APIRouter, HTTPException
from services.inbox_service import get_user_inbox
from services.inbox_service import get_user_outbox

router = APIRouter()

@router.get("/inboxLetter")
def inbox_letters(user_id: int):
    inbox_letters = get_user_inbox(user_id)
    if not inbox_letters:
        raise HTTPException(status_code=404, detail="No letters found in the inbox for the specified user ID")
    return inbox_letters

@router.get("/outboxLetter")
def outbox_letters(user_id: int):
    outbox_letters = get_user_outbox(user_id)
    if not outbox_letters:
        raise HTTPException(status_code=404, detail="No letters found in the outbox for the specified user ID")
    return outbox_letters
