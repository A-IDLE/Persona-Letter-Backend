from app.services.pinecone import pinecone_delete_namespace
from app.query.letter import delete_letter_by_userId_and_characterId

def delete_letters(user_id: int, character_id: int):
    
    # Delete the related letters from the SQL database
    delete_letter_by_userId_and_characterId(user_id, character_id)
    
    # Delete the related vectors from the Pinecone index
    pinecone_delete_namespace(user_id, character_id)
    
    return "Letters deleted successfully."