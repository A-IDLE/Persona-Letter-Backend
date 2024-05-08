from pydantic import BaseModel
from datetime import datetime

class LetterDto(BaseModel):
    character_id: int
    user_id: int
    letter_content: str
    created_date: datetime | None = None