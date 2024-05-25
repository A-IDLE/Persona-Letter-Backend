from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from app.services.prompt import load_prompt
from app.services.model import load_model, LLM
from langchain_community.callbacks.manager import get_openai_callback


def generate_questions(letter_content: str):

    full_path = "generate_questions_0.5"
    prompt_text = load_prompt(full_path)

    prompt = PromptTemplate.from_template(prompt_text)

    llm = LLM()

    llm_chain = (
        {"letter_content": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = llm_chain.invoke(letter_content)

    return response


def refining_retrieved_info(retrieved_info: str, letter_content: str):

    full_path = "refining_info_0.3"
    base_prompt = load_prompt(full_path)

    prompt_inputs = {
        'letter_content': "letter_content",
        'retrieved_info': retrieved_info,
    }

    prompt_text = base_prompt.format(**prompt_inputs)

    prompt = PromptTemplate.from_template(prompt_text)

    # 2. LLM
    llm = load_model()

    # 3. Chain
    chain = (
        {"letter_content": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    try:

        # response = chain.invoke(letter_content)

        with get_openai_callback() as cb:
            response = chain.invoke(letter_content)

            print(f"총 사용된 토큰수: \t\t{cb.total_tokens}")
            print(f"프롬프트에 사용된 토큰수: \t{cb.prompt_tokens}")
            print(f"답변에 사용된 토큰수: \t{cb.completion_tokens}")
            print(f"호출에 청구된 금액(USD): \t${cb.total_cost}")

        print("\n\n\n\nTHIS IS REFINED RETRIEVED INFO \n\n")
        print(response)
        print("-----"*10)
        print("check 123")
        print("\n\n\n\n")

        return response

    except Exception as e:
        ("An error occurred: " + str(e))
        pass


def verfiy_language(letter_content: str):

    print("come to verify language")
    print(letter_content)

    promt_text = """
        # Original Letter:
        {text}
        
        
       What is the language of the Original Letter?
        
        answer only in format below:
        
        #Format 
       English
    
    """

    prompt = PromptTemplate.from_template(promt_text)

    print("this is prompt")
    print(prompt)

    # 2. LLM
    llm = load_model()

    # 3. Chain
    chain = (
        {"text": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    try:
        print("come to try")

        # response = chain.invoke(letter_content)

        with get_openai_callback() as cb:
            response = chain.invoke(letter_content)

            print(f"총 사용된 토큰수: \t\t{cb.total_tokens}")
            print(f"프롬프트에 사용된 토큰수: \t{cb.prompt_tokens}")
            print(f"답변에 사용된 토큰수: \t{cb.completion_tokens}")
            print(f"호출에 청구된 금액(USD): \t${cb.total_cost}")

        print("come to response")
        print(response)

        prompt = (
            f"""\n\nWRITE ONLY IN {response}"""
        )

        print("\n\n\n\nTHE LANGUAGE \n\n")
        print(response)
        print("-----"*10)
        print("\n\n\n\n")

        return prompt

    except Exception as e:
        ("An error occurred: " + str(e))
        pass

    
### TEST FUNCTIONS ###
    
def generate_questions_test(letter_content: str, prompt_file: str) -> str:

    full_path = prompt_file
    prompt_text = load_prompt(full_path)

    prompt = PromptTemplate.from_template(prompt_text)

    llm = LLM()

    llm_chain = (
        {"letter_content": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # response = llm_chain.invoke(letter)

    with get_openai_callback() as cb:
        response = llm_chain.invoke(letter_content)

        print(f"총 사용된 토큰수: \t\t{cb.total_tokens}")
        print(f"프롬프트에 사용된 토큰수: \t{cb.prompt_tokens}")
        print(f"답변에 사용된 토큰수: \t{cb.completion_tokens}")
        print(f"호출에 청구된 금액(USD): \t${cb.total_cost}")

    return response


def refining_retrieved_info_test(retrieved_info: str, prompt_file: str) -> str:

    full_path = prompt_file
    prompt_text = load_prompt(full_path)

    prompt = PromptTemplate.from_template(prompt_text)

    # 2. LLM
    llm = load_model()

    # 3. Chain
    chain = (
        {"retrieved_info": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    try:

        # response = chain.invoke(retrieved_info)

        with get_openai_callback() as cb:
            response = chain.invoke(retrieved_info)

            print(f"총 사용된 토큰수: \t\t{cb.total_tokens}")
            print(f"프롬프트에 사용된 토큰수: \t{cb.prompt_tokens}")
            print(f"답변에 사용된 토큰수: \t{cb.completion_tokens}")
            print(f"호출에 청구된 금액(USD): \t${cb.total_cost}")

        print("\n\n\n\nTHIS IS REFINED RETRIEVED INFO \n\n")
        print(response)
        print("-----"*10)
        print("check 123")
        print("\n\n\n\n")

        return response

    except Exception as e:
        ("An error occurred: " + str(e))
        pass