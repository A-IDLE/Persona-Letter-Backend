import os
from pinecone import Pinecone
from dotenv import load_dotenv
from app.models.models import Letter
from app.utils.utils import advanced_preprocessing_by_llm
from app.services.embeddings import text_to_vector

load_dotenv()

class PineconeDB:
    
    def __init__(
        self,
        index_name = os.getenv('PINECONE_INDEX_NAME'), 
        pinecone_api_key = os.getenv('PINECONE_API_KEY')
    ):
        """_summary_

        Args:
            index_name (_type_, optional): _description_. Defaults to os.getenv('PINECONE_INDEX_NAME').
            pinecone_api_key (_type_, optional): _description_. Defaults to os.getenv('PINECONE_API_KEY').
        """
        
        self.index_name = index_name
        self.pinecone_api_key = pinecone_api_key
        self.index = self.pinecone_init()
        
    def pinecone_init(self):
        
        api_key = self.pinecone_api_key
        index_name = self.index_name
        
        if not all([api_key, index_name]):
            raise ValueError("Missing environment variables. Ensure PINECONE_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL, and OPENAI_API_KEY are set.")
        try:
            pc = Pinecone(api_key=api_key)
            index = pc.Index(index_name)
            return index
        except Exception as e:
            print(f"An error occurred while initializing the Pinecone index: {e}")
            return None
        
    def delete_namespace(
        self, 
        user_id: int, 
        character_id: int
    ):
        """_summary_

        Args:
            user_id (int): _description_
            character_id (int): _description_

        Returns:
            _type_: _description_
        """ 
        
        namespace = f"{user_id}_{character_id}"

        try:
            index = self.index
            response = index.delete(delete_all=True, namespace=namespace)
            print(f"Pinecone response: {response}")
            return response
        except Exception as e:
            print(f"An error occurred while deleting the namespace: {e}")
            return None
        
    def upsert_letter(
        self,
        letter: Letter
    ):

        letter_content = letter.letter_content
        
        print(f"this is embed_letter_pinecone_test {letter_content} \n\n") # log
        
        chunked_letter_content = advanced_preprocessing_by_llm(letter_content)

        vector_data = []
        namespace = f"{letter.user_id}_{letter.character_id}"
        embeddings = text_to_vector(chunked_letter_content)
        
        print(f"text_to_vector function completed for {len(embeddings['data'])} documents.") # log

        for idx, (text, vector) in enumerate(zip(chunked_letter_content, embeddings['data'])):
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

        index = self.index
        response = index.upsert(vector_data, namespace)

        return response
        
