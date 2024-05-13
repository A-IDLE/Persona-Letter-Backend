from services.letter import write_letter_character
from query.letter import Letter
from query.letter import get_letter_by_id
from services.embeddings import embed_letter, embed_letter_pinecone
from datetime import datetime
from schemas.schemas import LetterDto
from models.database import SessionLocal


def write_letter(letter: LetterDto):
    
    # 편지 객체 초기화
    letter_sending = Letter()
    
    letter_sending.character_id = letter.character_id
    letter_sending.user_id = letter.user_id
    letter_sending.reception_status = "sending"
    letter_sending.letter_content =  letter.letter_content
    letter_sending.created_time = datetime.now()
    
    letter_received = write_letter_character(letter_sending)
    
    save_letter(letter_sending)
    save_letter(letter_received)

    return letter_received



def save_letter(letter: Letter):
    try:
        with SessionLocal() as session:
            # embed_letter(letter)
            embed_letter_pinecone(letter)
            session.add(letter)
            session.commit()
            return "Letter saved successfully."
    except Exception as e:
        # The session is automatically rolled back by the context manager.
        return f"Error saving the letter: {str(e)}"
    

def get_a_letter(letter_id: int):
    return get_letter_by_id(letter_id)