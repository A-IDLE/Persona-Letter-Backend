from models.models import Character
from models.database import SessionLocal    
    
def create_character(character: Character):
    try:
        with SessionLocal() as session:
            session.add(character)
            session.commit()
            return character
    except Exception as e:
        return f"Error saving the character: {str(e)}"

def get_character_by_name(character_name: str):
    try:
        with SessionLocal() as session:
            character = session.query(Character).filter(Character.character_name == character_name).first()
            return character
    except Exception as e:
        return f"Error getting the character: {str(e)}"
    
def get_character_by_id(character_id: int):
    try:
        with SessionLocal() as session:
            character = session.query(Character).filter(Character.character_id == character_id).first()
            return character
    except Exception as e:
        return f"Error getting the character: {str(e)}"
    
def delete_user_by_id(character_id: int):
    try:
        with SessionLocal() as session:
            character = session.query(Character).filter(Character.character_id == character_id).first()
            session.delete(character)
            session.commit()
            return "Character deleted successfully."
    except Exception as e:
        return f"Error deleting the character: {str(e)}"