from models.models import User
from models.database import SessionLocal
from sqlalchemy.orm import Session

    
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
    
def get_user_by_id(user_id: int, db: Session):
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
    
def update_user_name(user_id: int, new_user_name: str):
    try:
        print(f"Attempting to update user {user_id} with name {new_user_name}")  # 함수 호출 확인 로그
        with SessionLocal() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.user_name = new_user_name
                session.commit()
                print(f"User {user_id} name updated to {new_user_name}")  # 성공 로그
                return "User name updated successfully."
            else:
                print(f"User {user_id} not found")  # 사용자 없음 로그
                return "User not found."
    except Exception as e:
        print(f"Error updating user name: {str(e)}")  # 에러 로그
        return f"Error updating the user name: {str(e)}"
    
def update_user_nickname(user_id: int, new_user_nickname: str):
    try:
        print(f"Attempting to update user {user_id} with name {new_user_nickname}")  # 함수 호출 확인 로그
        with SessionLocal() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.user_nickname = new_user_nickname
                session.commit()
                print(f"User {user_id} name updated to {new_user_nickname}")  # 성공 로그
                return "User nickname updated successfully."
            else:
                print(f"User {user_id} not found")  # 사용자 없음 로그
                return "User not found."
    except Exception as e:
        print(f"Error updating user nickname: {str(e)}")  # 에러 로그
        return f"Error updating the user nickname: {str(e)}"