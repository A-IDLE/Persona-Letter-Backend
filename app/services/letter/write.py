from datetime import datetime
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from requests import Session
from app.query.user import get_user_by_id
from app.services.prompt import load_character_prompt
from app.models.models import Letter
from app.query.character import get_character_by_id
from app.services.model import load_model
from .retrieve import retrieve_through_letter, retrieve_letter_test
from .generate import verfiy_language, refining_retrieved_info, generate_questions
from app.models.models import RagTestData
from app.query.test import create_test
from app.query.letter import get_letters_by_character_id
import json


def write_letter(letter_send: Letter, db: Session):

    # Extract the letter content, user_id, character_id
    letter_content = letter_send.letter_content
    user_id = letter_send.user_id
    character_id = letter_send.character_id
    
    # 관련된 정보를 retrieval을 통해서 가져온다
    related_letters = retrieve_through_letter(letter_content, user_id, character_id, db)

    related_letters_str = [f"Document content: {related_letter}" for related_letter in related_letters]

    refined_retrieved_info = refining_retrieved_info(related_letters_str, letter_content)

    language_prompt = verfiy_language(letter_content)
    
    print("\n this is language prompt\n\n")
    print(language_prompt)

    added_prompt = (
        f"""\n\n## REFERENCE INFO\n{refined_retrieved_info}"""
    )
    
    print("\nThis is added prompt\n\n")
    print(added_prompt)
    
    # character_id를 통해서 character 찾는다
    character = get_character_by_id(letter_send.character_id)
    # 검색된 character의 이름을 가져온다
    character_name = character.character_name

    # user_id를 통해서 user 정보 찾기
    user = get_user_by_id(user_id, db)
    user_name = user.user_name if user else 'User'
    user_nickname = user.user_nickname if user else 'User'
    
    print(f"user_name: {user_name}, user_nickname: {user_nickname}")  # 로그 추가
    
    # 1. Prompt
    character_prompt = load_character_prompt(character_name, letter_content, user_name, user_nickname)

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
    

def write_letter_test(letter_send: Letter, test: RagTestData):

    # Extract the letter content, user_id, character_id
    letter_content = letter_send.letter_content
    user_id = letter_send.user_id
    character_id = letter_send.character_id
    top_k = test.top_k
    
    # 관련된 정보를 retrieval을 통해서 가져온다
    # related_letters = retrieve_through_letter(letter_content, user_id, character_id)
    
    generated_questions = generate_questions(letter_content)
    generated_questions = json.loads(generated_questions)
    related_letters = retrieve_letter_test(generated_questions, user_id, character_id, top_k)

    related_letters_str = [f"Document content: {related_letter}" for related_letter in related_letters]

    refined_retrieved_info = refining_retrieved_info(related_letters_str, letter_content)

    language_prompt = verfiy_language(letter_content)
    
    print("\n this is language prompt\n\n")
    print(language_prompt)

    added_prompt = (
        f"""\n\n## REFERENCE INFO\n{refined_retrieved_info}"""
    )
    
    print("\nThis is added prompt\n\n")
    print(added_prompt)
    
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
        
        
        # Save the test data
        test.response_letter_content = response
        test.generated_questions = generated_questions
        test.retrieved_info = related_letters_str
        test.refined_info = refined_retrieved_info
        
        print(test)
        
        create_test(test)

        return letter_receiving

    except Exception as e:
        ("An error occurred: " + str(e))
        pass
    
    

def write_letter_history(letter_send: Letter):

    # Extract the letter content, user_id, character_id
    letter_content = letter_send.letter_content
    user_id = letter_send.user_id
    character_id = letter_send.character_id
   
    # check the language of the letter
    language_prompt = verfiy_language(letter_content)
    
    # Get previous letters from database and add it to the prompt
    previous_letters = get_letters_by_character_id(user_id, character_id)
    
    # Convert the previous letters to str - sending as User and receiving as Character
    previous_letters_str = "\n".join([f])
    # character_id를 통해서 character 찾는다
    character = get_character_by_id(letter_send.character_id)
    # 검색된 character의 이름을 가져온다
    character_name = character.character_name
    
    # 1. Prompt
    character_prompt = load_character_prompt(character_name, letter_content)

    # Include historical letters in the prompt
    final_prompt = f"Chat History:\n{previous_letters_str}\n\n" + character_prompt 
    
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
        print("An error occurred: " + str(e))
        pass

