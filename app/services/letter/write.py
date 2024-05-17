from datetime import datetime
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from services.prompt import load_character_prompt
from models.models import Letter
from query.character import get_character_by_id
from services.model import load_model
from .retrieve import retrieve_through_letter
from .generate import verfiy_language, refining_retrieved_info


def write_letter(letter_send: Letter):

    # Extract the letter content, user_id, character_id
    letter_content = letter_send.letter_content
    user_id = letter_send.user_id
    character_id = letter_send.character_id
    
    # 관련된 정보를 retrieval을 통해서 가져온다
    related_letters = retrieve_through_letter(letter_content, user_id, character_id)

    related_letters_str = [f"Document content: {related_letter}" for related_letter in related_letters]

    refined_retrieved_info = refining_retrieved_info(related_letters_str, letter_content)

    language_prompt = verfiy_language(letter_content)

    added_prompt = (
        f"""\n\n## REFERENCE INFO\n{refined_retrieved_info}"""
    )
    
    # character_id를 통해서 character 찾는다
    character = get_character_by_id(letter_send.character_id)
    # 검색된 character의 이름을 가져온다
    character_name = character.character_name

    # 1. Prompt
    character_prompt = load_character_prompt(character_name, letter_content)

    final_prompt = character_prompt + added_prompt + language_prompt

    prompt = PromptTemplate.from_template(final_prompt)

    print("\n\n\n\nTHIS IS FINAL PROMPT \n\n")
    print(final_prompt)
    print("\n\n"+"****"*10+"\n\n\n\n")

    # 2. LLM
    llm = load_model()

    # 3. Chain
    chain = (
        {"letter": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 4. Write Mail
    try:

        response = chain.invoke(letter_content)

        # 응답한 메일을 초기화
        letter_receiving = Letter()
        letter_receiving.character_id = character.character_id
        letter_receiving.user_id = letter_send.user_id
        letter_receiving.reception_status = "receiving"
        letter_receiving.letter_content = response
        letter_receiving.created_time = datetime.now()

        return letter_receiving

    except Exception as e:
        ("An error occurred: " + str(e))
        pass