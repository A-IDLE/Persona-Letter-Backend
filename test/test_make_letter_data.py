# Ensure the top-level project directory is in the Python path
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Add the root directory of the project to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.models import Letter
from app.services.letter.write import write_letter
from app.services.letter.save import save_letter
from app.query.character import get_character_by_id
from app.services.vector_database import pinecone_delete_namespace
from app.models.database import get_db


# Define the path of the letter directory
letter_dir = os.path.join(os.path.dirname(__file__),"data","letter")

def check_dir_exist(dir:str):    
    if not os.path.exists(dir):
        os.makedirs(dir)

def write_file(dir, content):
    with open(dir, 'w', encoding="utf-8") as file:
        file.write(content)
        

def test_file():
    
    check_dir_exist(letter_dir)
    
    for i in range(10):
        extension = ".txt"
        letter_name = f"test_letter_{i+1}{extension}"
        file_path = os.path.join(letter_dir, letter_name)
        
        
        content = f"This is content for letter {i+1}"
        
        write_file(file_path, content)
        
        
        
def replace_text_in_file():
    
    # Define the replacements
    replacements = {
        'Hermione': '{character_name}',
        '[Your Name]': '{user_name}'
    }
    
    for i in range(10):
        extension = ".txt"
        letter_name = f"test_letter_{i+1}{extension}"
        file_path = os.path.join(letter_dir, letter_name)
    
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Replace the specified text
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(content)
            
            
def delete_user_letters_from_pinecone():
    
    user_id = 123
    character_id = 2
    response = pinecone_delete_namespace(user_id, character_id)
    print(response)
    
    return response

            
def make_test_data():
    
    user_id = 123
    character_id = 2
    character_name = get_character_by_id(character_id).character_name 
    
    letter_dir = os.path.join(os.path.dirname(__file__),"data","letter")
    
     # Define the replacements
    replacements = {
        '{character_name}': character_name,
        '{user_name}' : "John"
    }
    
    for i in range(9):
        ext = ".txt"
        letter_name = f"test_letter_{i+1}{ext}"
        file_path = os.path.join(letter_dir, letter_name)
        
        with open(file_path, "r") as file:
            content = file.read()
            
        # Replace the specified text
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
            
        new_letter = Letter()
        new_letter.character_id = character_id
        new_letter.user_id = user_id
        new_letter.letter_content = content
        new_letter.reception_status = "sending"
        
        db =get_db()
        
        received_letter = write_letter(new_letter, db)
        
        
        print("saving process start")
        
        save_letter(new_letter)
        save_letter(received_letter)
        
        
        print("process done")
        
        
if __name__ == "__main__":
    make_test_data()
    # delete_user_letters_from_pinecone()