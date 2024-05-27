from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import EnsembleRetriever
from app.utils.utils import load_pdf, load_txt
from app.services.embeddings import text_to_vector
from app.services.vector_database import load_vector_db
from app.services.pinecone import pinecone_init
from dotenv import load_dotenv
import os

load_dotenv()


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
    contexts = []

    for question in questions:
        embedding_response = text_to_vector(question)
        if not embedding_response.get('data'):
            raise ValueError("Failed to generate embedding for the question.")
        
        question_embedding = embedding_response['data'][0]['embedding']
        retrieved_contexts = fetch_relevant_contexts(user_id, character_id, question_embedding)
        contexts.extend(retrieved_contexts)
        
    return contexts

def fetch_relevant_contexts(user_id, character_id, question_embedding):
    """
    Helper function to fetch relevant contexts with retries.

    Args:
        user_id (int): User ID
        character_id (int): Character ID
        question_embedding (list): Embedding of the question

    Returns:
        list: List of retrieved contexts
    """

    index = pinecone_init()
    namespace = f"{user_id}_{character_id}"
    contexts = []

    print("Fetching relevant contexts...")

    # response = index.query(index_name, namespace, question_embedding)
    response = index.query(
            namespace=namespace,
            vector=question_embedding,
            top_k=1,
            include_values=True,
            include_metadata=True
            )
    
    if not response.get('matches'):
        print("No matches found.")
        return contexts

    contexts.extend([match['metadata']['text'] for match in response['matches']])
    print(f"Retrieved {len(contexts)} contexts.")

    return contexts


## FOR TESTING
def get_pinecone_retriever_test(user_id: int, character_id: int, questions: [str], top_k: int):
    """
    Retrieve relevant contexts for specific user and character based on given questions.

    Args:
        user_id (int): User ID
        character_id (int): Character ID
        questions ([str]): List of questions

    Returns:
        list: List of relevant contexts
    """
    contexts = []

    for question in questions:
        embedding_response = text_to_vector(question)
        if not embedding_response.get('data'):
            raise ValueError("Failed to generate embedding for the question.")
        
        question_embedding = embedding_response['data'][0]['embedding']
        retrieved_contexts = fetch_relevant_contexts_test(user_id, character_id, question_embedding, top_k)
        contexts.extend(retrieved_contexts)
        
    return contexts

def fetch_relevant_contexts_test(user_id, character_id, question_embedding, top_k):
    """
    Helper function to fetch relevant contexts with retries.

    Args:
        user_id (int): User ID
        character_id (int): Character ID
        question_embedding (list): Embedding of the question

    Returns:
        list: List of retrieved contexts
    """

    index = pinecone_init()
    namespace = f"{user_id}_{character_id}"
    contexts = []

    print("Fetching relevant contexts...")

    # response = index.query(index_name, namespace, question_embedding)
    response = index.query(
            namespace=namespace,
            vector=question_embedding,
            top_k=top_k,
            include_values=True,
            include_metadata=True
            )
    
    if not response.get('matches'):
        print("No matches found.")
        return contexts

    contexts.extend([match['metadata']['text'] for match in response['matches']])
    print(f"Retrieved {len(contexts)} contexts.")

    return contexts


class PineconeRetriever:
    def __init__(self, top_k:int = 5):
        self.index = pinecone_init()
        self.top_k = top_k
        
        
    def retrieve(self, user_id: int, character_id: int, questions: [str], top_k: int = None):
        """
        Retrieve relevant contexts for specific user and character based on given questions.

        Args:
            user_id (int): User ID
            character_id (int): Character ID
            questions ([str]): List of questions
            top_k (int): Number of top results to fetch

        Returns:
            list: List of relevant contexts
        """
        
        ## If top_k is not provided, use the default value
        if not top_k:
            top_k = self.top_k
        
        contexts = []

        for question in questions:
            embedding_response = text_to_vector(question)
            if not embedding_response.get('data'):
                raise ValueError("Failed to generate embedding for the question.")
            
            question_embedding = embedding_response['data'][0]['embedding']
            retrieved_contexts = self.fetch_relevant_contexts(user_id, character_id, question_embedding, top_k)
            contexts.extend(retrieved_contexts)
            
        return contexts

    def fetch_relevant_contexts(self, user_id, character_id, question_embedding, top_k):
        """
        Helper function to fetch relevant contexts with retries.

        Args:
            user_id (int): User ID
            character_id (int): Character ID
            question_embedding (list): Embedding of the question
            top_k (int): Number of top results to fetch

        Returns:
            list: List of retrieved contexts
        """
        namespace = f"{user_id}_{character_id}"
        contexts = []

        print("Fetching relevant contexts...")

        response = self.index.query(
                namespace=namespace,
                vector=question_embedding,
                top_k=top_k,
                include_values=True,
                include_metadata=True
                )
        
        if not response.get('matches'):
            print("No matches found.")
            return contexts

        contexts.extend([match['metadata']['text'] for match in response['matches']])
        print(f"Retrieved {len(contexts)} contexts.")

        return contexts


