from fastapi import APIRouter
from services.character_service import get_characters

router = APIRouter()

@router.get("/characters")
def getCharacters():

    characters = get_characters()
    
    return characters