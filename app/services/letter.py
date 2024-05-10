from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from services.retriever import load_faiss_retriever, load_tuned_faiss_retriever
from services.model import load_model
from utils.utils import document_to_string, load_prompt
from services.prompt import load_character_prompt
from datetime import datetime
from models.models import Letter
from repository.character import get_character_by_id
        

def generate_questions(letter):
    # # 총 몇개의 질문을 만들지
    # max_questions = 3

    # prompt_text = """
    #         You are an AI assistant tasked with generation of 3 questions to explore deeper based on the following letter
            
    #         ## Letter
    #         {letter}
            
    #         Please answer in format only, without any other content.
            
    #         """
            
            
    prompt_text = """
        You are an AI assistant tasked with using a given format to find the content that needs to be searched for a given context.
        Please answer in format only, without any other content. Please find at least 3 and no more than 10 items.
        Returns the found contents as a Python list.
        #question:
        {question}
            
            """
            
            
    # prompt_text = """
    # #user's letter:
    # {question}
    
    
    # These are the steps that you need to follow
    # ## Step 1
    # Extract the main keywords/topics from the user's letter.
    # ## Step 2
    # Extract the user's intent from the user's letter.
    # ## Step 3
    # Based on the user's interest in [Keywords/Topics] and their intent to [Intent], answer in the format below.
    
    # #format:
    # keyword/topics:
    
    # intent:
        
    # """
            
            
            
            
    prompt = PromptTemplate.from_template(prompt_text)

    llm = load_model()
    
    llm_chain = (
         {"question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = llm_chain.with_config(configuarble={"llm":"gpt-4-turbo-preview"}).invoke(letter)
    return response


def retrieve_letter(questions:str, user_id:int, character_id:int):
    retriever = load_tuned_faiss_retriever(user_id, character_id)
    letters = retriever.invoke(questions)
    
    print("\n\n\n\nTHIS IS RETRIEVED LETTERS \n"+"****"*10)
    for letter in letters:
        
        print("\n\n")
        print(letter.page_content)
        print("\n\n")
        
    print("RETRIEVAL DONE \n\n\n\n"+"****"*10)
    

    return letters


def retrieve_through_letter(letter_content: str, user_id: int, character_id: int):
     ## 2-1. 수신 메일에 대한 질의 작성
    questions = generate_questions(letter_content)

    ## 2-2. 질의 내용을 RAG를 통해서 관련 메일 추출
    related_letters = retrieve_letter(questions, user_id, character_id)
    
    return related_letters

def write_letter(letter):
    # 1. Embed the received Letter
    
    related_letters = retrieve_through_letter(letter)
    related_letters_str = [document_to_string(related_letter) for related_letter in related_letters]
    
    added_prompt =(
        f"""
        
        ## Reference
        {related_letters_str}
        
        """ 
    )

    
    ## 1. Prompt
    file_name = "hermione_markdown_including_pottermore"
    
    hermione_prompt = load_prompt(file_name)
    final_prompt = hermione_prompt + added_prompt
    
    prompt = PromptTemplate.from_template(final_prompt)
    
    
   
    
    
    ## 2. LLM
    llm = load_model()
    
    ## 3. Chain
    chain = (
        { "letter": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # 4. Write Mail
    try:
        
        response = chain.invoke(letter)

        return response
    
    except Exception as e:
        ("An error occurred: " + str(e))
        pass
    
    
def write_letter_character(letter_send: Letter):
    
    # Extract the letter content, user_id, character_id
    letter_content = letter_send.letter_content
    user_id = letter_send.user_id
    character_id = letter_send.character_id
    
    # character_id를 통해서 character 찾는다
    character = get_character_by_id(letter_send.character_id)
    
    character_name = character.character_name
    
    related_letters = retrieve_through_letter(letter_content, user_id, character_id)
    
    related_letters_str = [document_to_string(related_letter) for related_letter in related_letters]
    
    refined_retrieved_info = refining_retrieved_info(related_letters_str, letter_content)
    
    
    
    added_prompt =(
        f"""\n\n## REFERENCE INFO\n{refined_retrieved_info}""")

    
    ## 1. Prompt
    character_prompt = load_character_prompt(character_name)
    
    final_prompt = character_prompt + added_prompt
    
    prompt = PromptTemplate.from_template(final_prompt)
    
    
    
    print("\n\n\n\nTHIS IS FINAL PROMPT \n\n")
    print(final_prompt)
    print("\n\n"+"****"*10+"\n\n\n\n")
    
    
    # print("THIS IS FINAL PROMPT \n\n")
    # print(prompt)
    
    
    ## 2. LLM
    llm = load_model()
    
    ## 3. Chain
    chain = (
        { "letter": RunnablePassthrough()}
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
    

def refining_retrieved_info(retrieved_info: str, letter_content: str):
    
    promt_text = f"""
        # Original Letter:
        {letter_content}
        
        
        # Retrieved_info:
        {retrieved_info}
        
        from above delete all the retrieved info that is not relevant to the original letter.
        
        answer only in format below:
        
        #Format
        - info1
        - info2
        - info3
    
    """
    
    prompt = PromptTemplate.from_template(promt_text)
    
    ## 2. LLM
    llm = load_model()
    
    ## 3. Chain
    chain = (
        { "letter_content": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        
        response = chain.invoke(letter_content)
        
        
        print("\n\n\n\nTHIS IS REFINED RETRIEVED INFO \n\n")
        print(response)
        print("-----"*10)
        print("check 123")
        print("\n\n\n\n")

        return response
    
    except Exception as e:
        ("An error occurred: " + str(e))
        pass
    