from models.database import SessionLocal
from models.models import Letter, Character
from sqlalchemy.orm import Session

def create_letter(letter: Letter):
    try:
        with SessionLocal() as session:
            session.add(letter)
            session.commit()
            return letter
    except Exception as e:
        return f"Error saving the letter: {str(e)}"

def get_a_letter(letter_id: int):
    try:
        with SessionLocal() as session:
            letter = session.query(Letter).filter(Letter.letter_id == letter_id).first()
            return letter
    except Exception as e:
        return f"Error getting the letter: {str(e)}"


def get_letters_by_character_id(user_id: int, character_id: int, db: Session):

    try:
        letters = db.query(Letter).filter(
            Letter.user_id == user_id, Letter.character_id == character_id).all()
        return letters
    except Exception as e:
        return f"Error getting letters for user and character: {str(e)}"

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
    
    
def get_letters_by_user_id_and_character_id(user_id: int, character_id: int):
    try:
        with SessionLocal() as session:
            letters = session.query(Letter).filter(Letter.user_id == user_id, Letter.character_id == character_id).all()
            return letters
    except Exception as e:
        return f"Error getting letters for user and character: {str(e)}"
    
    
def get_letters_by_reception_status(user_id: int, character_id: int, reception_status: str):
    try:
        with SessionLocal() as session:  
            # Letter 테이블과 Character 테이블을 조인하고 필요한 정보를 선택합니다.
            letters = session.query(
                Letter, Character.character_name
            ).join(
                Character, Letter.character_id == Character.character_id
            ).filter(
                Letter.user_id == user_id, 
                Letter.character_id == character_id,  # 클릭한 캐릭터 아이디와 일치하는 메일만 가져옵니다.
                Letter.reception_status == reception_status
            ).all()

            # 결과를 딕셔너리 형태로 포맷하여 리스트에 추가합니다.
            result = []
            for letter, character_name in letters:
                letter_info = {
                    "letter_id": letter.letter_id,
                    "character_name": character_name,
                    "letter_content": letter.letter_content,
                    "letter_image_status": 0,
                    "read_status": letter.read_status,
                    "created_time": letter.created_time,
                    # 추가적으로 필요한 Letter 필드를 여기에 포함시킬 수 있습니다.
                }
                result.append(letter_info)

            return result
    except Exception as e:
        print("삐빅에러",e)  # 오류가 발생하면 오류 메시지를 출력합니다.
        return None
    
    
