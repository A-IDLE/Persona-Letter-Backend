from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from .base import Base


# Set up logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# 연결 DB 정의
# DB_URL = 'sqlite:///todo.sqlite3'


# Load environment variables from .env file
load_dotenv()

# Retrieve values from environment variables
print("COME ON BABY")
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
db_name = os.getenv('db_name')

print(user)
print(db_name)


DB_URL = f"mysql+pymysql://{user}:{password}@{host}:3306/{db_name}"


# 데이터베이스에 연결하는 엔진을 생성하는 함수
# Do you have check_same_thread=True in the url? Otherwise sqlalchemy does not passes it to mysql
engine = create_engine(DB_URL)
# engine = create_engine(DB_URL, connect_args={'check_same_thread': True})

# 데이터베이스와 상호 작용하는 세션을 생성하는 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 선언적 모델링을 위한 기본 클래스
base = Base


def init_db():
    """Create database tables."""
    
    Base.metadata.create_all(engine)

# 조회
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()