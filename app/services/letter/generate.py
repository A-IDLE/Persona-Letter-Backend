from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from app.services.prompt import load_prompt, load_prompt_file
from app.services.model import load_model, LLM
from langchain_community.callbacks.manager import get_openai_callback


def generate_questions(
    letter_content: str,
    prompt_file: str = "generate_questions_0.5"
) -> str:

    prompt = load_prompt_file(prompt_file)
    
    llm = LLM()

    llm_chain = (
        {"letter_content": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = llm_chain.invoke(letter_content)
    
    print(f"\n\n\n\nTHIS IS GENERATED QUESTIONS\n\n{response}\n\n")

    return response


def refining_retrieved_info(
    questions: str,
    retrieved_info: str, 
    prompt_file: str = "refining_info_0.7"    
) -> str:

    base_prompt = load_prompt(prompt_file)

    prompt_inputs = {
        'questions': questions,
        'retrieved_info': '{retrieved_info}',
    }

    prompt_text = base_prompt.format(**prompt_inputs)
    
    print(f"this is prompt_text\n\n{prompt_text}\n\n")

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

        response = chain.invoke(retrieved_info)

        print(f"\n\n\n\nTHIS IS REFINED RETRIEVED INFO \n\n{response}\n\n")

        return response

    except Exception as e:
        ("An error occurred: " + str(e))
        pass


def verfiy_language(
    letter_content: str,
    prompt_file: str = "verify_language"
) -> str:
    
    prompt = load_prompt_file(prompt_file)

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
        response = chain.invoke(letter_content)
        language_prompt = (f"""\n\nWRITE ONLY IN {response}""")

        return language_prompt

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


def refining_retrieved_info_test(
    questions: str,
    retrieved_info: str, 
    prompt_file: str
) -> str:
    
    base_prompt = load_prompt(prompt_file)

    prompt_inputs = {
        'questions': questions,
        'retrieved_info': '{retrieved_info}',
    }

    prompt_text = base_prompt.format(**prompt_inputs)
    
    print(f"this is prompt_text\n\n{prompt_text}\n\n")

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
    

def check_ambiguous_questions(
    questions: str,
    prompt_file: str = "check_ambiguous_questions_0.2"
    
) -> str:
        
        prompt = load_prompt_file(prompt_file)
    
        # 2. LLM
        llm = load_model()
    
        # 3. Chain
        chain = (
            {"questions": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
    
        try:
            response = chain.invoke(questions)
            
            print(f"\n\nThis is the questions\n\n{questions}\n\n")
            print(f"Result of check_ambiguous_questions: \n\n{response}\n\n")
    
            return response
    
        except Exception as e:
            ("An error occurred: " + str(e))
            pass