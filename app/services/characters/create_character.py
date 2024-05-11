# CHARACTER RELATED
from models.models import Character
from services.model import load_make_character_model
from services.prompt import load_prompt
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from query.character import create_character


def parse_character_description(description, character_name):
    sections = description.split("## ")
    character = Character()
    character.character_name = character_name

    for section in sections[1:]:  # skip the first empty section
        title_end = section.find('\n')
        title = section[:title_end].strip()
        content = section[title_end:].strip()

        if title == "Biography":
            character.biography = content
        elif title == "Physical Description":
            character.physical_description = content
        elif title == "Personality and Traits":
            character.personality_and_trait = content
        elif title == "Magical Abilities and Skills":
            character.magical_abilities_and_skills = content
        elif title == "Possessions":
            character.possessions = content
        elif title == "Relationships":
            character.relationships = content
        elif title == "Etymology":
            character.etymology = content
        elif title == "Examples of Tone of Voice":
            character.examples_tone_of_voice = content

    return character

def get_character_info(character):
    
    # 1. prompt
    base_prompt = load_prompt("make_character") 
    
    print("prompt loaded")
    print(base_prompt)
    
    prompt = PromptTemplate.from_template(base_prompt)
    
    # 2. model
    llm = load_make_character_model()
    
    # 3. chain
    chain = (
        {"character": RunnablePassthrough()}
        |prompt
        |llm
        | StrOutputParser()
    )
    
    result = chain.invoke(character)
    
    return result


def create_character_by_character_name(character_name):
    print("시작합니다")
    # character_name = input("Write the Character that you want to create : ")
    character_info = get_character_info(character_name)
    print(character_info)
    character = parse_character_description(character_info,character_name)
    saved_character = create_character(character)
    print(saved_character)
    print("Character Saved!!")