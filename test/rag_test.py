import sys
import os

# Ensure the top-level project directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.models import Letter
from app.services.letter.write import write_letter_test, write_letter_history
from app.query.character import get_character_by_id
from app.models.models import RagTestData
from datetime import datetime
from app.models.database import init_db

def rag_test():
    
    init_db()  
    
    user_id = 123
    character_id = 2
    
    letter_dir = os.path.join(os.path.dirname(__file__),"data","letter","test_letter_easy.txt")
    
    character_name = get_character_by_id(character_id).character_name 
    
    with open(letter_dir, 'r') as file:
        content = file.read()
        
        replacements = {
            '{character_name}': character_name,
            '{user_name}' : "John"
        }
        
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)

    # Test Data initialization
    test = RagTestData()
    test.created_time = datetime.now()
    test.version = "0.5"
    test.changes = "changed preprocessing process set no duplicate info, implemented window slidding method for chunking"
    test.request_letter_content = content
    test.response_letter_content = ""
    test.chunk_size = 200
    test.chunk_overlap = 0
    test.top_k = 5
    test.filter = ""
    test.basic_character_prompt = "form_0.2.md"
    test.generate_questions_prompts = "generate_questions_0.4"
    test.generated_questions = ""
    test.refining_retrieved_info_prompt = "refining_info_0.4"
    test.refined_info = ""
    test.notes = ""
        
    request_letter = Letter()
    request_letter.user_id = user_id
    request_letter.character_id = character_id
    request_letter.letter_content = content
    request_letter.reception_status = "sending"
    
    response_letter = write_letter_test(request_letter, test)
    
    # response_letter = write_letter_history(request_letter)
    
    return "TEST DONE"





if __name__ == "__main__":
    
    # for i in range(3):
    #     rag_test()
    
    rag_test()