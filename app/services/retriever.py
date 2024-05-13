from dotenv import load_dotenv
import openai
from services.vector_database import load_vector_db, load_cached_db
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import EnsembleRetriever
from utils.utils import load_pdf, load_txt
from pinecone import Pinecone
from openai import OpenAI
import os
import time


def load_faiss_retriever():
    # db = load_vector_db()
    # faiss_retriever = db.as_retriever(serach_type="mmr", search_kwargs={"k":20})

    db = load_vector_db()

    faiss_retriever = db.as_retriever(search_type="mmr", search_kwargs={
        "k": 20,
        "filter": {'reception_status': 'sending'}
    })

    return faiss_retriever


def load_bm25_retriever(path):

    # splitter 설정
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=150)

    pdf_documents = load_pdf(path) if path else []
    pdf_docs = splitter.split_documents(
        pdf_documents) if pdf_documents else []  # 업로드된 파일 쪼개기
    print(f"PDF의 총 문서수 : {len(pdf_docs)}")

    # .txt 파일 업로드
    txt_documents = load_txt(path) if path else []
    txt_docs = splitter.split_documents(
        txt_documents) if txt_documents else []  # 업로드된 파일 쪼개기
    print(f".txt의 총 문서수 : {len(txt_docs)}")

    # .pdf 과 .txt 병합
    combined_docs = pdf_docs + txt_docs

    bm25_retriever = BM25Retriever.from_documents(
        combined_docs
    )

    # 검색시 최대 3개의 결과를 반환하도록 한다
    bm25_retriever.k = 1

    return bm25_retriever


def load_ensemble_retriever(path):

    faiss_retriever = load_faiss_retriever()
    bm25_retriever = load_bm25_retriever(path)

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.6, 0.4],
        search_type="mmr",
    )

    return ensemble_retriever


def load_tuned_faiss_retriever(user_id: int, character_id: int):
    """
    특정 사용자와 캐릭터에 대한 튜닝된 faiss retriever를 반환합니다.
    
    Returns a tuned faiss retriever for a specific user and character.
    
    Args:
        user_id (int): 사용자 id
        character_id (int): 캐릭터 id
    """

    db = load_vector_db()

    faiss_retriever = db.as_retriever(search_type="mmr", search_kwargs={
        "k": 30,
        "filter": {
            'reception_status': 'sending',
            'user_id': user_id,
            'character_id': character_id
        }
    })

    return faiss_retriever

def get_pinecone_retriever(user_id: int, character_id: int, questions:[str]):
    """
    특정 사용자와 캐릭터에 대한 pinecone retriever 결과를 반환합니다.
    
    Args:
        user_id (int): 사용자 id
        character_id (int): 캐릭터 id
        questions ([str]): 질문들
    """

    load_dotenv()   # 환경변수들 불러오기
    api_key = os.getenv('PINECONE_API_KEY') # pinecone api key
    index_name = os.getenv('PINECONE_INDEX_NAME')  # db index 이름
    embedding_model = os.getenv('EMBEDDING_MODEL') #  embedding 모델

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    # get relevant contexts
    contexts = []

    time_waited = 0
    client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    )
    for question in questions:
        xq = client.embeddings.create(
            input=question,
            model=embedding_model,
            encoding_format="float"
        ).data[0].embedding

        while (len(contexts) < 3 and time_waited < 10):
            res = index.query(
            namespace=f"{user_id}_{character_id}",
            vector=xq,
            top_k=3,
            include_metadata=True
            )
            contexts = contexts + [
                x['metadata']['text'] for x in res['matches']
            ]
            print(f"Retrieved {len(contexts)} contexts, sleeping for 5 seconds...")
            time.sleep(5)
            time_waited += 5

        if time_waited >= 10:
            print("Timed out waiting for contexts to be retrieved.")
            contexts = ["No contexts retrieved. Try to answer the question yourself!"]

    print(f"contexts: {contexts}")

    return contexts