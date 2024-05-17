from services.vector_database import pinecone_delete_namespace
from services.letter import write_letter_character
from query.letter import Letter
from query.letter import get_letter_by_id
from services.embeddings import embed_letter, embed_letter_pinecone
from datetime import datetime
from schemas.schemas import LetterDto
from models.database import SessionLocal


def write_letter(letter: LetterDto):

    # pinecone_delete_namespace() # 테스트용 코드
    
    # 편지 객체 초기화
    letter_sending = Letter()
    
    letter_sending.character_id = letter.character_id
    letter_sending.user_id = letter.user_id
    letter_sending.reception_status = "sending"
    letter_sending.letter_content =  letter.letter_content
    letter_sending.created_time = datetime.now()
    
    letter_received = write_letter_character(letter_sending)
    # letter_receiving = Letter()
    # letter_receiving.character_id = letter.character_id
    # letter_receiving.user_id = letter.user_id
    # letter_receiving.reception_status = "receiving"
#     letter_receiving.letter_content = """**Dear Inji,**
# Hermione Granger"""
    # letter_receiving.created_time = datetime.now()

    
    save_letter(letter_sending)
    save_letter(letter_received)

    return letter_received



def save_letter(letter: Letter):
    try:
        with SessionLocal() as session:
            # embed_letter(letter)
            session.add(letter)
            session.commit()
            result = embed_letter_pinecone(letter)
            print(f"save_letter result : {result}")
            return "Letter saved successfully."
    except Exception as e:
        # The session is automatically rolled back by the context manager.
        return f"Error saving the letter: {str(e)}"
    

def get_a_letter(letter_id: int):
    return get_letter_by_id(letter_id)