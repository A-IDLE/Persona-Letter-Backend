from pydantic import BaseModel
from datetime import datetime

class LetterDto(BaseModel):
    character_id: int
    user_id: int
    letter_content: str
    reception_status : str | None = None
    created_date: datetime | None = None

class CharacterDto(BaseModel):
    character_id: int
    character_name: str
    biography: str | None = None
    physical_description: str | None = None
    personality_and_trait: str | None = None
    magical_abilities_and_skills: str | None = None
    possessions: str | None = None
    relationships: str | None = None
    etymology: str | None = None
    examples_tone_of_voice: str | None = None
    character_image_url: str | None = None
    series: str | None = None
    created_time: datetime | None = None
    updated_time: datetime | None = None