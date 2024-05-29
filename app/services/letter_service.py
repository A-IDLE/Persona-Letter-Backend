
from app.services.image.send import sqs_message
from app.services.vector_database import pinecone_delete_namespace
from app.services.embeddings import embed_letter_pinecone
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.schemas import LetterDto
from app.services.letter.write import write_letter, write_letter_update, write_letter_history
from app.services.letter.save import save_letter
from app.query.letter import Letter
from app.query.letter import get_a_letter
from app.query.letter import get_received_letter as query_get_received_letter


def create_letter(letter: LetterDto, db: Session):

    # pinecone_delete_namespace("6_3") # 테스트용 코드
    
    # 편지 객체 초기화
    letter_sending = Letter()
    
    letter_sending.character_id = letter.character_id
    letter_sending.user_id = letter.user_id
    letter_sending.reception_status = "sending"
    letter_sending.letter_content =  letter.letter_content
    letter_sending.created_time = datetime.now()
    
    letter_received = write_letter(letter_sending, db)

    
    save_letter(letter_sending)
    save_letter(letter_received)

    sqs_message(letter_received) # 이미지 생성 요청

    return letter_received



# def save_letter(letter: Letter):
#     try:
#         with SessionLocal() as session:
#             # embed_letter(letter)
            
#             # DB에 저장 (insert)
#             session.add(letter)
#             session.commit()
            
#             # Pinecone 서비스를 이용하여 벡터를 저장
#             result = embed_letter_pinecone(letter)
#             print(f"save_letter result : {result}")
#             return "Letter saved successfully."
#     except Exception as e:
#         # The session is automatically rolled back by the context manager.
#         return f"Error saving the letter: {str(e)}"
    

def get_a_letter(letter_id: int, db: Session):
    return get_a_letter(letter_id)

def get_received_letter(letter_id: int, db: Session):
    return query_get_received_letter(letter_id, db)

def create_letter_update(letter: LetterDto):
    
    # 편지 객체 초기화
    letter_sending = Letter()
    letter_sending.character_id = letter.character_id
    letter_sending.user_id = letter.user_id
    letter_sending.reception_status = "sending"
    letter_sending.letter_content =  letter.letter_content
    letter_sending.created_time = datetime.now()
    
    letter_received = write_letter_update(letter_sending)
    # letter_received = write_letter_history(letter_sending)
    
    save_letter(letter_sending)
    save_letter(letter_received)

    sqs_message(letter_received) # 이미지 생성 요청

    return letter_received