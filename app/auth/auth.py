import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from fastapi import Depends, HTTPException, Security, APIRouter, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from pydantic import BaseModel
from app.services.auth.auth_service import google_login, update_user_name_after_login, get_user_name, update_user_nickname_after_login


router = APIRouter(prefix="/api")

cred = credentials.Certificate("serviceAccountKey.json")
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

        # print(authorization)
        token = authorization.split(" ")[1] if len(authorization.split(" ")) == 2 else None
        
        # print(token)
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

class UpdateUserNameRequest(BaseModel):
    accessToken: str
    new_user_name: str

class UpdateUserNicknameRequest(BaseModel):
    accessToken: str
    new_user_nickname: str

async def google_login_pretreatment(token_data: TokenData):
    try:
        ## Extract the token from the request body
        accessToken = token_data.accessToken
        
        print("accessToken FINE")
        print(accessToken)
        # Verify the token
        user_info = auth.verify_id_token(accessToken)
        
        print("user_info FINE")
        
        return user_info
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/login/google")
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


@router.post("/validateToken")
def confirm_accessToken(token_data: TokenData):
    try:
        ## Extract the token from the request body
        accessToken = token_data.accessToken
        
        print("accessToken FINE")
        # print(accessToken)
        # Verify the token
        user_info = auth.verify_id_token(accessToken)
        
        print("user_info FINE")
        
        return user_info
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/userInfo")
async def get_user_info(request: Request):
    try:
        user_info = request.state.user
        if not user_info:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        return {
            "user_id": user_info.get("uid"),
            "name": user_info.get("name"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/updateUser")
def update_user(request: UpdateUserNameRequest):
    try:
        token_data = TokenData(accessToken=request.accessToken)
        print(f"Received request to update user with new name {request.new_user_name}")  # 요청 확인 로그
        result = update_user_name_after_login(token_data, request.new_user_name)
        return {"message": result}
    except Exception as e:
        print(f"Error in update_user endpoint: {str(e)}")  # 에러 로그
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/updateUserNickname")
def update_user(request: UpdateUserNicknameRequest):
    try:
        token_data = TokenData(accessToken=request.accessToken)
        print(f"Received request to update user with new nickname {request.new_user_nickname}")  # 요청 확인 로그
        result = update_user_nickname_after_login(token_data, request.new_user_nickname)
        return {"message": result}
    except Exception as e:
        print(f"Error in update_user endpoint: {str(e)}")  # 에러 로그
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getUserName")
def get_user_name_endpoint(token: HTTPAuthorizationCredentials = Security(security)):
    try:
        token_data = TokenData(accessToken=token.credentials)
        user_name = get_user_name(token_data)
        return user_name
    except Exception as e:
        print(f"Error in get_user_name endpoint: {str(e)}")  # 에러 로그
        raise HTTPException(status_code=500, detail=str(e))