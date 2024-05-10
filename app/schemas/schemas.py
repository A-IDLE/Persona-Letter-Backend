from pydantic import BaseModel
from datetime import datetime

class LetterDto(BaseModel):
    character_id: int
    user_id: int
    letter_content: str
    created_date: datetime | None = None

class CharacterDto(BaseModel):
    character_id: int
    character_name: str
    biography: str
    physical_description: str
    personality_and_trait: str
    magical_abilities_and_skills: str
    possessions: str
    relationships: str
    etymology: str
    examples_tone_of_voice: str
    character_image_url: str
    series: str
    created_time: datetime | None = None
    updated_time: datetime | None = None