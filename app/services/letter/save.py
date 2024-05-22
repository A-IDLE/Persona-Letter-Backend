from requests import Session
from app.models.models import Letter
from app.models.database import SessionLocal
from app.services.embeddings import embed_letter_pinecone



def save_letter(letter: Letter, db: Session):
    try:
        with SessionLocal() as session:
            # embed_letter(letter)
            
            # DB에 저장 (insert)
            session.add(letter)
            session.commit()
            
            # Pinecone 서비스를 이용하여 벡터를 저장
            result = embed_letter_pinecone(letter)
            print(f"save_letter result : {result}")
            return "Letter saved successfully."
    except Exception as e:
        # The session is automatically rolled back by the context manager.
        return f"Error saving the letter: {str(e)}"