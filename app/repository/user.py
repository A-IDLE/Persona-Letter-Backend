from models.models import User
from models.models import SessionLocal
    
def create_user(user: User):
    try:
        with SessionLocal() as session:
            session.add(user)
            session.commit()
            return user
    except Exception as e:
        return f"Error saving the user: {str(e)}"

def get_user_by_email(email: str):
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.email == email).first()
            return user
    except Exception as e:
        return f"Error getting the user: {str(e)}"
    
def get_user_by_id(user_id: int):
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            return user
    except Exception as e:
        return f"Error getting the user: {str(e)}"
    
def delete_user_by_id(user_id: int):
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            session.delete(user)
            session.commit()
            return "User deleted successfully."
    except Exception as e:
        return f"Error deleting the user: {str(e)}"