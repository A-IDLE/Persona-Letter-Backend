from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_core.documents.base import Document
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

def init_vectorDB():
     # 환경변수들 불러오기
    load_dotenv()
    vector_db_path = os.getenv('VECTOR_DB_PATH')  # vector db 의 경로
    DB_INDEX = os.getenv('DB_INDEX')  # db index 이름
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') #  embedding 모델
    vector_db_path_faiss = vector_db_path + "/DB_INDEX.faiss"
    
     # 사용할 embedding 모델
    embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    docs =[]
    doc = Document(page_content="")
    docs.append(doc)

     # vector db 가 있는 경우
    if os.path.exists(vector_db_path_faiss):
        # vector db를 불러온다
        db = load_vector_db()

        # 불러온 db에 벡터 추가
        db2 = FAISS.from_documents(docs, embeddings_model)
        db.merge_from(db2)

        # db 저장
        db.save_local(
            folder_path= vector_db_path,
            index_name= DB_INDEX,
        )

        print("FAISS database updated and saved.")
    else:
        # Initialize the database
        db = FAISS.from_documents(docs, embeddings_model)
        # db 저장
        db.save_local(
            folder_path=vector_db_path,
            index_name=DB_INDEX,
        )

        print("new FAISS database saved.")