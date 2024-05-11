from query.user import get_user_by_email, create_user
from models.models import User

def google_login(email: str):
    
    # Check if the user is already registered
    user = get_user_by_email(email)
    
    if(user):
        return user
    else:
        register_user = User(email=email)
        create_user(register_user)
        new_user = get_user_by_email(email)
        return new_user
        