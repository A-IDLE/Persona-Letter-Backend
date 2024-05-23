from app.models.models import RagTestData
from app.models.database import SessionLocal
from sqlalchemy.orm import Session

    
def create_test(test: RagTestData):
    db: Session = SessionLocal()
    try:
        db.add(test)
        db.commit()
        db.refresh(test)
    except Exception as e:
        db.rollback()
        print(f"An error occurred while saving the test data: {e}")
    finally:
        db.close()