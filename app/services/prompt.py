from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from services.model import load_make_character_model
from query.character import get_character_by_name


###### PROMPT LOADER
def load_prompt(file_name):
    
    root_path = "services/prompt/"
    full_path = root_path+file_name+".md"
    
    print("loading prompt")
    print(full_path)
    
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except Exception as e:
        print("Error has Occured")
        print(e)
        pass


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


def load_character_prompt(character_name, letter_content):
    
    character = get_character_by_name(character_name)
    
    print(character)
    
    prompt_inputs = {
        'character_name': character.character_name,
        'biography': character.biography,
        'physical_description': character.personality_and_trait,
        'magical_abilities_and_skills': character.magical_abilities_and_skills,
        'personality_and_traits': character.personality_and_trait,
        'relationships': character.relationships,
        'possessions': character.possessions,
        'etymology': character .etymology,
        'examples_tone_of_voice':  character.examples_tone_of_voice,
        'letter':  letter_content,
    }
    
    base_prompt = load_prompt("hermione_markdown_0.2.1")
    
    final_prompt = base_prompt.format(**prompt_inputs)
    
    return final_prompt
    
    




    