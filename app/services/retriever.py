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

# def get_pinecone_retriever(user_id: int, character_id: int, questions:[str]):
#     """
#     특정 사용자와 캐릭터에 대한 pinecone retriever 결과를 반환합니다.
    
#     Args:
#         user_id (int): 사용자 id
#         character_id (int): 캐릭터 id
#         questions ([str]): 질문들
#     """

#     load_dotenv()   # 환경변수들 불러오기
#     api_key = os.getenv('PINECONE_API_KEY') # pinecone api key
#     index_name = os.getenv('PINECONE_INDEX_NAME')  # db index 이름
#     embedding_model = os.getenv('EMBEDDING_MODEL') #  embedding 모델

#     pc = Pinecone(api_key=api_key)
#     index = pc.Index(index_name)

#     # get relevant contexts
#     contexts = []

#     time_waited = 0
#     client = OpenAI(
#     api_key = os.getenv("OPENAI_API_KEY"),
#     )
#     for question in questions:
#         xq = client.embeddings.create(
#             input=question,
#             model=embedding_model,
#             encoding_format="float"
#         ).data[0].embedding

#         while (len(contexts) < 3 and time_waited < 10):
#             res = index.query(
#             namespace=f"{user_id}_{character_id}",
#             vector=xq,
#             top_k=3,
#             include_metadata=True
#             )
#             contexts = contexts + [
#                 x['metadata']['text'] for x in res['matches']
#             ]
#             print(f"Retrieved {len(contexts)} contexts, sleeping for 5 seconds...")
#             time.sleep(5)
#             time_waited += 5

#         if time_waited >= 10:
#             print("Timed out waiting for contexts to be retrieved.")
#             contexts = ["No contexts retrieved. Try to answer the question yourself!"]

#     print(f"contexts: {contexts}")

#     return contexts

import os
import requests
from dotenv import load_dotenv

class PineconeClient:
    def __init__(self, api_key, index_host):
        self.api_key = api_key
        self.index_host = index_host

    def query(self, index_name, namespace, vector, top_k=3, include_metadata=True):
        headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "vector": vector,
            "top_k": top_k,
            "include_metadata": include_metadata,
            "namespace": namespace
        }
        response = requests.post(f"{self.index_host}/query", headers=headers, json=payload)
        response_data = response.json()
        return response_data

    def upsert(self, index_name, vectors):
        headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "vectors": vectors
        }
        response = requests.post(f"{self.index_host}/vectors/upsert", headers=headers, json=payload)
        response_data = response.json()
        return response_data

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.openai.com/v1/embeddings"

    def create_embedding(self, input_text, model):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "input": input_text,
            "model": model,
            "encoding_format": "float"
        }
        response = requests.post(self.endpoint, headers=headers, json=payload)
        response_data = response.json()
        return response_data

def get_pinecone_retriever(user_id: int, character_id: int, questions: [str]):
    """
    Retrieve relevant contexts for specific user and character based on given questions.

    Args:
        user_id (int): User ID
        character_id (int): Character ID
        questions ([str]): List of questions

    Returns:
        list: List of relevant contexts
    """
    load_dotenv()  # Load environment variables

    api_key = os.getenv('PINECONE_API_KEY')
    index_name = os.getenv('PINECONE_INDEX_NAME')
    embedding_model = os.getenv('EMBEDDING_MODEL')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    index_host = os.getenv('PINECONE_INDEX_HOST')

    if not all([api_key, index_name, embedding_model, openai_api_key]):
        raise ValueError("Missing environment variables. Ensure PINECONE_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL, and OPENAI_API_KEY are set.")

    pinecone_client = PineconeClient(api_key=api_key, index_host=index_host)
    openai_client = OpenAIClient(api_key=openai_api_key)

    contexts = []

    print(f"Retrieving contexts for user {user_id} and character {character_id}...")

    for question in questions:
        embedding_response = openai_client.create_embedding(question, embedding_model)
        if not embedding_response.get('data'):
            raise ValueError("Failed to generate embedding for the question.")
        
        question_embedding = embedding_response['data'][0]['embedding']
        retrieved_contexts = fetch_relevant_contexts(pinecone_client, index_name, user_id, character_id, question_embedding)
        contexts.extend(retrieved_contexts)

    print(f"Retrieved contexts: {contexts}")
    return contexts

def fetch_relevant_contexts(pinecone_client, index_name, user_id, character_id, question_embedding, max_contexts=5):
    """
    Helper function to fetch relevant contexts with retries.

    Args:
        pinecone_client (PineconeClient): Pinecone client instance
        index_name (str): Pinecone index name
        user_id (int): User ID
        character_id (int): Character ID
        question_embedding (list): Embedding of the question
        max_retries (int): Maximum number of retries
        sleep_interval (int): Sleep interval between retries in seconds
        max_contexts (int): Maximum number of contexts to retrieve

    Returns:
        list: List of retrieved contexts
    """
    namespace = f"{user_id}_{character_id}"
    contexts = []

    print("Fetching relevant contexts...")

    while len(contexts) < max_contexts:
        response = pinecone_client.query(index_name, namespace, question_embedding)
        print(f"Response: {response}")

        contexts.extend([match['metadata']['text'] for match in response['matches']])
        if len(contexts) >= max_contexts:
            break
    
    if len(contexts) < max_contexts:
        print("Unable to retrieve sufficient contexts within the retry limit.")
        return ["No contexts retrieved. Try to answer the question yourself!"]

    return contexts
