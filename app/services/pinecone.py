from dotenv import load_dotenv
import os
from pinecone import Pinecone


def pinecone_upsert(vector_data, namespace):
    # upsert vector data into the Pinecone index
    try:
        # Configure Pinecone client
        index = pinecone_init()
        response = index.upsert(vectors=vector_data, namespace=namespace)  # Upsert the vector data into the index
        print(f"Pinecone response: {response}")
        return response
    except Exception as e:
        print(f"An error occurred while upserting vectors: {e}")
        return None
    
def pinecone_init():
    # Initialize the Pinecone index
    load_dotenv()
    api_key = os.getenv('PINECONE_API_KEY')
    index_name = os.getenv('PINECONE_INDEX_NAME')
    if not all([api_key, index_name]):
        raise ValueError("Missing environment variables. Ensure PINECONE_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL, and OPENAI_API_KEY are set.")
    try:
        # Configure Pinecone client
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)
        return index
    except Exception as e:
        print(f"An error occurred while initializing the Pinecone index: {e}")
        return None

def pinecone_delete_namespace(user_id: int, character_id: int):
    """_summary_

    Args:
        user_id (int): _description_
        character_id (int): _description_

    Returns:
        _type_: _description_
    """
    
    namespace = f"{user_id}_{character_id}"

    # Delete a namespace from the Pinecone index
    try:
        # Configure Pinecone client
        index = pinecone_init()
        response = index.delete(delete_all=True, namespace=namespace)
        print(f"Pinecone response: {response}")
        return response
    except Exception as e:
        print(f"An error occurred while deleting the namespace: {e}")
        return None