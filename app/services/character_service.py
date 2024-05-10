from repository.character import Character, get_all_characters_for_main
from schemas.schemas import CharacterDto
from models.database import SessionLocal
import json
from collections import defaultdict

def get_characters():
    characters = get_all_characters_for_main()
    # print(characters)
    # Convert to the desired JSON format
    # Prepare a dictionary to hold series data
    series_dict = defaultdict(list)

    # Populate the dictionary with characters grouped by series
    for series, character_id, character_image_url, character_name in characters:
        series_dict[series].append({
            "character_id": str(character_id),
            "character_name": character_name,
            "character_image_url": character_image_url if character_image_url is not None else "No image available"
        })

    # Create a list of dictionaries for each series
    output_data = [
        {
            "series": series_name,
            "characters": characters
        }
        for series_name, characters in series_dict.items()
    ]

    print(output_data)

    return output_data
