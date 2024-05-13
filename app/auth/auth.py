import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from fastapi import Depends, HTTPException, Security, APIRouter, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth.auth_service import google_login
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from pydantic import BaseModel



router = APIRouter()

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)


security = HTTPBearer()

## AUTH MIDDLEWARE
class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths=None):
        super().__init__(app)
        self.excluded_paths = set(excluded_paths or [])

    async def dispatch(self, request: Request, call_next):
        # Skip middleware for excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return Response("Authorization header is required", status_code=401)

        print(authorization)
        token = authorization.split(" ")[1] if len(authorization.split(" ")) == 2 else None
        
        print(token)
        if not token:
            return Response("Bearer token not found", status_code=401)

        try:
            # Verify the ID token
            user_info = auth.verify_id_token(token)
            # Attach the decoded token to the request state
            request.state.user = user_info
        except auth.InvalidIdTokenError:
            return Response("Invalid ID token", status_code=401)
        except Exception as e:
            return Response(f"An error occurred: {str(e)}", status_code=500)

        return await call_next(request)




def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token.credentials)
        uid = decoded_token['uid']
        return auth.get_user(uid)
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")
    
    
### GOOGLE LOGIN

class TokenData(BaseModel):
    accessToken: str

async def google_login_pretreatment(token_data: TokenData):
    try:
        ## Extract the token from the request body
        accessToken = token_data.accessToken

        # Verify the token
        user_info = auth.verify_id_token(accessToken)
        
        return user_info
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/googleLogin")
def get_user_data(user_info = Depends(google_login_pretreatment)):
    
    ## Extract email from the user_info
    email = user_info.get("email")
    
    ## Perform google login with the email
    user = google_login(email)
    
    # 유저 아이디를 응답으로 보낸다.
    response = {
        "userId":user.user_id
    }
    
    
    return response


@router.get("/test")
def test(request: Request):
    user_info = request.state.user
    email = user_info.get("email")
    print(email)
    return {"email": email}
