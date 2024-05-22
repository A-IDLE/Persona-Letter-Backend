from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings
from langchain_core.documents.base import Document
from langchain.storage import LocalFileStore
from openai import OpenAI
from openai import OpenAIError
import os
from app.utils.utils import load_pdf, load_txt, identify_path
from app.services.vector_database import load_vector_db, pinecone_upsert
from app.models.models import Letter



def embedding_data(data):
    # data 가 pdf 인경우
    if identify_path(data):
        embed_docs(data)
    # data 가 text(str) 인경우
    else:
        embed_text(data)




def embed_text(text):
    # 환경변수들 불러오기
    load_dotenv()
    vector_db_path = os.getenv('VECTOR_DB_PATH')  # vector db 의 경로
    DB_INDEX = os.getenv('DB_INDEX')  # db index 이름
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') #  embedding 모델

    # 사용할 embedding 모델
    embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    docs =[]
    doc = Document(page_content=text)
    docs.append(doc)

     # vector db 가 있는 경우
    if os.path.exists(vector_db_path):
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
        # 없는 경우 만든다
        os.makedirs(vector_db_path)
        # Embed texts
        db = FAISS.from_documents(docs, embeddings_model)
        # db 저장
        db.save_local(
            folder_path=vector_db_path,
            index_name=DB_INDEX,
        )

        print("new FAISS database saved.")


# 문서의 경로를 입력받아 해당 경로의 파일들을 임베딩하는 def
def embed_docs(docs_path):
    """
        param = path
        해당 경로에 있는 
        .pdf 파일과 .txt 파일을 embedding, 그리고 cache
    """ 

    # 환경변수들 불러오기
    load_dotenv()
    vector_db_path = os.getenv('VECTOR_DB_PATH')  # vector db 의 경로
    CACHE_DB_INDEX = os.getenv('CACHE_DB_INDEX')  # db index 이름
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') #  embedding 모델

    # 사용할 embedding 모델
    embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    # splitter 설정
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)

    ## .pdf 파일 업로드
    pdf_documents = load_pdf(docs_path) if docs_path else []
    pdf_docs = splitter.split_documents(pdf_documents) if pdf_documents else [] # 업로드된 파일 쪼개기
    print(f"PDF의 총 문서수 : {len(pdf_docs)}")
    
    ## .txt 파일 업로드
    txt_documents = load_txt(docs_path) if docs_path else []
    txt_docs = splitter.split_documents(txt_documents) if txt_documents else [] # 업로드된 파일 쪼개기
    print(f".txt의 총 문서수 : {len(txt_docs)}")

    # .pdf 과 .txt 병합
    combined_docs = pdf_docs + txt_docs

    # 캐시될 파일 위치
    store = LocalFileStore("./cache")

    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embeddings_model, store, namespace=EMBEDDING_MODEL
    )

    db = FAISS.from_documents(combined_docs, cached_embeddings)

    # db 저장
    db.save_local(
        folder_path= vector_db_path,
        index_name= CACHE_DB_INDEX,
    )
    
def embed_letter(letter: Letter):
    
    # 환경변수들 불러오기
    load_dotenv()
    vector_db_path = os.getenv('VECTOR_DB_PATH')  # vector db 의 경로
    DB_INDEX = os.getenv('DB_INDEX')  # db index 이름
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') #  embedding 모델
    embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL) # 사용할 embedding 모델
    
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
    
    
    docs =[]
    doc = Document(
        page_content=letter.letter_content,
        metadata={
            "character_id":letter.character_id,
            "user_id":letter.user_id,
            "reception_status":letter.reception_status,
            "created_time":letter.created_time,
        }
    )
    
    docs.append(doc)
    
    
    split_docs = splitter.split_documents(docs) if docs else [] # 업로드된 파일 쪼개기
    print(f"\n\nSPLIT DOCS 총 문서수 : {len(split_docs)}\n\n")
    
    print("EMBEDDING LETTER++++++++++++++++++++++++++++++")

    # vector db 가 있는 경우
    if os.path.exists(vector_db_path):
        print("vector db exists")
        # vector db를 불러온다
        db = load_vector_db()

        # 불러온 db에 벡터 추가
        db2 = FAISS.from_documents(split_docs, embeddings_model)
        db.merge_from(db2)

        # db 저장
        db.save_local(
            folder_path= vector_db_path,
            index_name= DB_INDEX,
        )

        print("FAISS database updated and saved.")
    else:
        print()
        # 없는 경우 만든다
        os.makedirs(vector_db_path)
        # Embed texts
        db = FAISS.from_documents(split_docs, embeddings_model)
        # db 저장
        db.save_local(
            folder_path=vector_db_path,
            index_name=DB_INDEX,
        )

        print("new FAISS database saved.")
            

def embed_letter_pinecone(letter: Letter):
    # Initialize the text splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0, length_function=len, separators=["\n", ". "])

    # Split the document
    split_texts = splitter.split_text(letter.letter_content)
    print(f"\n\n embed_letter_pinecone SPLIT DOCS total documents: {len(split_texts)}\n\n")

    # Convert split documents to vectors
    vector_data = []
    namespace = f"{letter.user_id}_{letter.character_id}"
    embeddings = text_to_vector(split_texts)  # Get embeddings for all texts at once
    print(f"text_to_vector function completed for {len(embeddings['data'])} documents.")

    for idx, (text, vector) in enumerate(zip(split_texts, embeddings['data'])):
        vector_entry = {
            "id": f"{letter.letter_id}_{idx}",  # Creating a composite ID
            "values": vector['embedding'],
            "metadata": {
                "letter_id": letter.letter_id,
                "character_id": letter.character_id,
                "user_id": letter.user_id,
                "reception_status": letter.reception_status,
                "created_time": letter.created_time,
                "text": text,
            },
        }
        vector_data.append(vector_entry)

    # upsert vector data into the Pinecone index
    response = pinecone_upsert(vector_data, namespace)

    return response

# Example function to convert text to vector
def text_to_vector(texts):
    try:
        load_dotenv()
        model = os.getenv('EMBEDDING_MODEL')
        client = OpenAI()
        embeddings = client.embeddings.create(
            model=model,
            input=texts,
            encoding_format="float"
        )
        embeddings = embeddings.to_dict()
        print(f"Text to vector function completed for {len(embeddings['data'])} documents.")
        return embeddings
    except OpenAIError as e:
        print(f"An error occurred while generating embeddings: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None