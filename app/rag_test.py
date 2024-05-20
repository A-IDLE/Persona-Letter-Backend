import os
from models.models import Letter
from services.letter.write import write_letter
from query.character import get_character_by_id

def rag_test():
    
    user_id = 123
    character_id = 2
    
    letter_dir = os.path.join(os.path.dirname(__file__),"test","data","letter","test_letter_last.txt")
    
    character_name = get_character_by_id(character_id).character_name 
    
    with open(letter_dir, 'r') as file:
        content = file.read()
        
        replacements = {
            '{character_name}': character_name,
            '{user_name}' : "John"
        }
        
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
            
        
        
    print(content)
        
    request_letter = Letter()
    request_letter.user_id = user_id
    request_letter.character_id = character_id
    request_letter.letter_content = content
    request_letter.reception_status = "sending"
    
    response_letter = write_letter(request_letter)
    
    print("\n\n"+"****"*10+"\n\n")
    
    print("\n\nThis is response letter\n\n")
    print(response_letter.letter_content)
    
    print("\n\n"+"****"*10+"\n\n")
    
    return "TEST DONE"


if __name__ == "__main__":
    rag_test()