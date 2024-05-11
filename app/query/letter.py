from models.database import SessionLocal
from models.models import Letter

def create_letter(letter: Letter):
    try:
        with SessionLocal() as session:
            session.add(letter)
            session.commit()
            return letter
    except Exception as e:
        return f"Error saving the letter: {str(e)}"

def get_letter_by_id(letter_id: int):
    try:
        with SessionLocal() as session:
            letter = session.query(Letter).filter(Letter.letter_id == letter_id).first()
            return letter
    except Exception as e:
        return f"Error getting the letter: {str(e)}"

def get_letters_by_character(character_id: int):
    try:
        with SessionLocal() as session:
            letters = session.query(Letter).filter(Letter.character_id == character_id).all()
            return letters
    except Exception as e:
        return f"Error getting letters for character: {str(e)}"

def get_letters_by_user(user_id: int):
    try:
        with SessionLocal() as session:
            letters = session.query(Letter).filter(Letter.user_id == user_id).all()
            return letters
    except Exception as e:
        return f"Error getting letters for user: {str(e)}"

def update_letter_read_status(letter_id: int, read_status: bool):
    try:
        with SessionLocal() as session:
            letter = session.query(Letter).filter(Letter.letter_id == letter_id).first()
            if letter:
                letter.read_status = read_status
                session.commit()
                return "Letter read status updated successfully."
            else:
                return "Letter not found."
    except Exception as e:
        return f"Error updating letter read status: {str(e)}"

def delete_letter_by_id(letter_id: int):
    try:
        with SessionLocal() as session:
            letter = session.query(Letter).filter(Letter.letter_id == letter_id).first()
            if letter:
                session.delete(letter)
                session.commit()
                return "Letter deleted successfully."
            else:
                return "Letter not found."
    except Exception as e:
        return f"Error deleting the letter: {str(e)}"