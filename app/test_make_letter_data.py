import os

# Add the root directory of the project to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.models import Letter
from services.letter.write import write_letter
from services.letter.save import save_letter
from query.character import get_character_by_id


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


            
def make_test_data():
    
    user_id = 123
    character_id = 2
    character_name = get_character_by_id(character_id).character_name 
    
    letter_dir = os.path.join(os.path.dirname(__file__),"test","data","letter")
    
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
        
        received_letter = write_letter(new_letter)
        
        save_letter(new_letter)
        save_letter(received_letter)
        
        
if __name__ == "__main__":
    make_test_data()