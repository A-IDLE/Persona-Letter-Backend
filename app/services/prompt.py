from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.services.model import load_make_character_model
from app.query.character import get_character_by_name


###### PROMPT LOADER
def load_prompt(file_name):
    
    root_path = "app/services/prompt/"
    full_path = root_path+file_name+".md"    
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except Exception as e:
        print("Error has Occured")
        print(e)
        pass
    
def load_prompt_file(file_name:str) -> PromptTemplate:
    prompt_text = load_prompt(file_name)
    prompt = PromptTemplate.from_template(prompt_text)
    
    return prompt


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


def load_character_prompt(
    character_name: str, 
    letter_content: str, 
    user_name: str, 
    user_nickname: str,
    character_id: int,
    prompt_file: str = "form_0.5"
):
    # Determine the prompt file based on character_id
    if character_id == 2:
        prompt_file = "hermione_markdown_0.3.2"
    else:
        prompt_file = "form_0.5"
    
    print(f"Loading prompt file: {prompt_file}")

    character = get_character_by_name(character_name)
    
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
        'user_name': user_name,
        'user_nickname': user_nickname
    }

    base_prompt = load_prompt(prompt_file)
    final_prompt = base_prompt.format(**prompt_inputs)
    
    return final_prompt  