import os
import logging
from langchain_community.document_loaders import PyPDFLoader 
from langchain_community.document_loaders import TextLoader
from fastapi import Request
from query.user import get_user_by_email


###### LOADER

### PDF Loader
def load_pdf(path):
    pdf_documents = []  # List to hold all documents

    for dirpath, dirnames, filenames in os.walk(path):
        # Loop through each file in the directory
        for file in filenames:
            if file.endswith(".pdf"):
                # Build the full path to the file
                full_path = os.path.join(dirpath, file)
                try:
                    # Load the PDF file (assuming PyPDFLoader is correctly defined)
                    loader = PyPDFLoader(full_path)  # Removed encoding parameter
                    # Assuming the loader has a method to return documents as text
                    documents = loader.load()
                    pdf_documents.extend(documents)
                except Exception as e:
                    # Log the exception with the filename that caused it
                    logging.error(f"Failed to load {full_path}: {str(e)}")

    return pdf_documents


### Text Loader
def load_txt(path):
    txt_documents = []

     # .txt 파일 업로드
    for dirpath, dirnames, filenames in  os.walk(path):
        # 각 디렉토리에서 파일 목록을 확인한다
        for file in filenames:
            # TextLoader를 사용하여 파일의 전체 경로를 지어하고 문서를 로드합니다.
            if(file.endswith(".txt")) :

                full_path = os.path.join(dirpath, file)
                try:
                    # TextLoader를 사용하여 파일의 전체 경로를 지정하고 문서를 로드합니다.
                    loader = TextLoader(full_path, encoding="utf-8")
                    # 로드한 문서를 분할하여 documents 리스트에 추가합니다
                    txt_documents.extend(loader.load())
                except Exception as e:
                    # 파일 로드 중 오류가 발생하면 이를 무시하고 계속 진행합니다.
                   logging.error(f"Failed to load {full_path}: {str(e)}")



###### PATH IDENTIFIER
def identify_path(param):
    """
        if param is dir_path return True,
        else return False
    """
    # Check if the parameter is a dir
    if os.path.isdir(param):
        return True
    else:
        return False
    
    
###### PROMPT LOADER
def load_prompt(file_name):
    
    root_path = "prompt/"
    full_path = root_path+file_name+".md"
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except Exception as e:
        print("Error has Occured")
        pass
    

def document_to_string(doc):
    return f"Document content: {doc.page_content}"



def get_user_id_from_request(request:Request):
    # Request 객체에서 user_id를 추출합니다.
    email = request.state.user.get("email")
    user = get_user_by_email(email)
    user_id = user.user_id
    
    return user_id

def get_email_from_request(request:Request):
    # Request 객체에서 email 추출합니다.
    email = request.state.user.get("email")
    
    return email