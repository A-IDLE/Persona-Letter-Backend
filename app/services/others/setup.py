
from services.characters.create_character import create_character_by_character_name
from query.character import get_character_by_name

def character_setup_by_names(characters_names):
    """
    Create characters based on a list of names, if they do not already exist.

    Args:
        characters_names (list of str): A list of character names to potentially create.
    """
    
    for character_name in characters_names:
        character = get_character_by_name(character_name)
        print("CHARACTER VALIDATION")
        print(character_name)
        print(character.character_name)
        if character:
            print(f"Character {character_name} already exists")           
        else:
            print("Does not exist")
            create_character_by_character_name(character_name)
            
