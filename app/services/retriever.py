from services.vector_database import load_vector_db, load_cached_db
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import EnsembleRetriever
from utils.utils import load_pdf, load_txt



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
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)

    pdf_documents = load_pdf(path) if path else []
    pdf_docs = splitter.split_documents(pdf_documents) if pdf_documents else [] # 업로드된 파일 쪼개기
    print(f"PDF의 총 문서수 : {len(pdf_docs)}")
    
    ## .txt 파일 업로드
    txt_documents = load_txt(path) if path else []
    txt_docs = splitter.split_documents(txt_documents) if txt_documents else [] # 업로드된 파일 쪼개기
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
        retrievers = [bm25_retriever, faiss_retriever],
        weights = [0.6, 0.4],
        search_type="mmr",
    )

    return ensemble_retriever