from app.models.models import Letter
from app.models.database import SessionLocal
from app.services.embeddings import embed_letter_pinecone, embed_letter_pinecone_test
from app.database.vectorDB.pinecone_database import PineconeDB



def save_letter(letter: Letter):
    try:
        with SessionLocal() as session:
            session.add(letter)
            session.commit()
            db = PineconeDB()
            result = db.upsert_letter(letter)
            return "Letter saved successfully."
    except Exception as e:
        return f"Error saving the letter: {str(e)}"