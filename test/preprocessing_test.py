# Ensure the top-level project directory is in the Python path
import os
import sys
from app.services.letter.generate import advanced_preprocessing_by_llm
from app.models.models import Letter
from app.services.letter.write import write_letter_test, write_letter_history
from app.query.character import get_character_by_id
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


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

    return "TEST DONE"


if __name__ == "__main__":

    # for i in range(3):
    #     rag_test()

    preprocessing_test()
