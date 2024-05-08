from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
import os
from dotenv import load_dotenv
import logging

class ExtendedFAISS(FAISS):
    def __init__(self, model, logger=None):
        super().__init__()
        self.embedding_model = model  # Assume an embedding model is required
        self.logger = logger or logging.getLogger(__name__)

    def _embed_query(self, text):
        # Ensure that this method correctly uses the callable to generate embeddings.
        return self.embedding_function(text)

    def save():
        return



def load_vector_db():
     # 환경변수들 불러오기
    load_dotenv()
    vector_db_path = os.getenv('VECTOR_DB_PATH')  # vector db 의 경로
    DB_INDEX = os.getenv('DB_INDEX')  # db index 이름
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') #  embedding 모델
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    db = FAISS.load_local(
            folder_path = vector_db_path,
            embeddings = embeddings,
            index_name= DB_INDEX,
            allow_dangerous_deserialization=True
    )

    return db



def load_cached_db():
     # 환경변수들 불러오기
    load_dotenv()
    vector_db_path = os.getenv('VECTOR_DB_PATH')  # vector db 의 경로
    CACHE_DB_INDEX = os.getenv('CACHE_DB_INDEX')  # db index 이름
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') #  embedding 모델

    store = LocalFileStore("./cache/")
    # OpenAI 임베딩 모델 인스턴스를 생성합니다. 모델명으로 "text-embedding-3-small"을 사용한다
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, disallowed_special=())
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embeddings, store, namespace=embeddings.model
    )

    db = FAISS.load_local(
            folder_path = vector_db_path,
            embeddings = cached_embeddings,
            index_name= CACHE_DB_INDEX,
            allow_dangerous_deserialization=True
    )

    return db