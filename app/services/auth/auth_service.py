from query.user import get_user_by_email, create_user, update_user_name, update_user_nickname  # update_user_name 추가
from models.models import User
from pydantic import BaseModel
from firebase_admin import auth
from fastapi import HTTPException

class TokenData(BaseModel):
    accessToken: str

def google_login(email: str):
    # Check if the user is already registered
    user = get_user_by_email(email)
    
    if user:
        return user
    else:
        register_user = User(email=email)
        create_user(register_user)
        new_user = get_user_by_email(email)
        return new_user

def get_user_data(token_data: TokenData):
    try:
        decoded_token = auth.verify_id_token(token_data.accessToken)
        email = decoded_token['email']
        print(f"Decoded token for email: {email}")  # 이메일 확인 로그
        return {"email": email}
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")

def update_user_name_after_login(token_data: TokenData, new_user_name: str):
    try:
        user_info = get_user_data(token_data)
        email = user_info.get("email")
        print(f"Updating user with email {email} to new name {new_user_name}")  # 함수 호출 확인 로그
        user = get_user_by_email(email)
        if user:
            result = update_user_name(user.user_id, new_user_name)
            if "Error" in result:
                raise Exception(result)
            return result
        else:
            raise Exception("User not found")
    except Exception as e:
        print(f"Error in update_user_name_after_login: {str(e)}")  # 에러 로그
        return f"Error updating user name: {str(e)}"
    
def update_user_nickname_after_login(token_data: TokenData, new_user_nickname: str):
    try:
        user_info = get_user_data(token_data)
        email = user_info.get("email")
        print(f"Updating user with email {email} to new nickname {new_user_nickname}")  # 함수 호출 확인 로그
        user = get_user_by_email(email)
        if user:
            result = update_user_nickname(user.user_id, new_user_nickname)
            if "Error" in result:
                raise Exception(result)
            return result
        else:
            raise Exception("User not found")
    except Exception as e:
        print(f"Error in update_user_nickname_after_login: {str(e)}")  # 에러 로그
        return f"Error updating user nickname: {str(e)}"
    
def get_user_name(token_data: TokenData):
    try:
        user_info = get_user_data(token_data)
        email = user_info.get("email")
        user = get_user_by_email(email)
        if user:
            return {"user_name": user.user_name}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))