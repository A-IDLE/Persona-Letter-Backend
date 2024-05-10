from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
from api.endpoints.write_letter import router
from models.database import init_db
from models import *
from services.others.setup import character_setup_by_names
from services.vector_database import init_vectorDB
from fastapi.middleware.cors import CORSMiddleware

fastapi_app = FastAPI()

# Initialize the database
init_db()  
init_vectorDB()

# Mount the router
fastapi_app.include_router(router)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# CORS 미들웨어 설정
# react와 fastapi 연결해주는 수단
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 허용할 출처 지정
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
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