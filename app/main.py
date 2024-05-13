from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어 임포트
from dotenv import load_dotenv
from pathlib import Path
# ROUTERS
from api.endpoints.get_a_letter import router as router3
from api.endpoints.inbox_letter import router as router_inbox
from api.endpoints.letter_router import router
from api.endpoints.character_router import router as router_character
from auth.auth import router as router_auth
# from api.router import router
from models.database import init_db
from models import *
from services.others.setup import character_setup_by_names
from services.vector_database import init_vectorDB
from fastapi.middleware.cors import CORSMiddleware
from auth.auth import AuthMiddleware
from services.mail.mail import router as router_mail

# 맥 오류 해결 Error #15: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

fastapi_app = FastAPI()

# 인증토큰 검증을 하지 않을 경로 설정
excluded_paths = [
    "/googleLogin",
    "/characters",
    "/sendmail",
    "/"
]

# 인증 미들웨어 추가
fastapi_app.add_middleware(AuthMiddleware, excluded_paths=excluded_paths)

# CORS 설정 추가
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React 앱의 호스트와 포트
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# Initialize the database
init_db()  
init_vectorDB()

# Mount the router
fastapi_app.include_router(router)
fastapi_app.include_router(router3)
fastapi_app.include_router(router_character)
fastapi_app.include_router(router_inbox)
fastapi_app.include_router(router_auth)
fastapi_app.include_router(router_mail)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Set up CORS middleware configuration
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List the origins that should be allowed, use ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# characters_names = [
#     "Harry Potter",
#     "Hermione Granger",
#     "Ron Weasley",
#     "Albus Dumbledore",
#     "Severus Snape",
#     "Sirius Black",
#     "Luna Lovegood",
#     "Rubeus Hagrid",
#     "Voldemort",
#     "Dobby",
#     "Ginny Weasley"
# ]


# character_setup_by_names(characters_names)


if __name__ == "__main__":
    uvicorn.run('main:fastapi_app',
                host='localhost', port=9000, reload=True)