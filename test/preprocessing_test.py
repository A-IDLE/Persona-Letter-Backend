# Ensure the top-level project directory is in the Python path
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from app.models.models import Letter
from app.services.letter.write import write_letter_test, write_letter_history
from app.utils.utils import advanced_preprocessing_by_llm
from app.query.character import get_character_by_id
import re



def preprocessing_test():

    user_id = 123
    character_id = 2

    letter_dir = os.path.join(os.path.dirname(
        __file__), "data", "letter", "test_letter_9.txt")

    character_name = get_character_by_id(character_id).character_name

    with open(letter_dir, 'r') as file:
        content = file.read()

        replacements = {
            '{character_name}': character_name,
            '{user_name}': "John"
        }

        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)

    letter = Letter()
    letter.user_id = user_id
    letter.character_id = character_id
    letter.letter_content = content
    letter.reception_status = "sending"

    response = advanced_preprocessing_by_llm(letter)

    print(response)

    return response

# Function to extract chunks from the input text
def extract_chunks(input_text):
    # Find all chunks using regular expressions
    chunks_data = re.findall(r'\[Chunk \d+\]\n\n(.+?)(?=\n\n\[Chunk \d+\]|\Z)', input_text, re.S)

    # Initialize an empty list to store the chunks
    chunks = []

    # Append each chunk to the list, stripping any leading/trailing whitespace
    for chunk in chunks_data:
        chunks.append(chunk.strip())

    return chunks




if __name__ == "__main__":

    # for i in range(3):
    #     rag_test()

    response = preprocessing_test()
    
    # Extract the chunks
    chunks = extract_chunks(response)

    # Display the chunks
    for idx, chunk in enumerate(chunks):
        print(f"chunks[{idx}] = {chunk}")
