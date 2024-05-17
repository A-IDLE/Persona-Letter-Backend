from services.model import load_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

def generate_questions(letter):

    prompt_text = """
        You are an AI assistant tasked with using a given format to find the content that needs to be searched for a given context.
        Please answer in format only, without any other content. Please find at least 3 and no more than 10 items.
        Returns the found contents as a Python list.
        #question:
        {question}
        
        #example answer format:
        ["found content1", "found content2", "found content3", "found content4", "found content5"]
            """

    prompt = PromptTemplate.from_template(prompt_text)

    llm = load_model()

    llm_chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = llm_chain.with_config(configuarble={"llm":"gpt-4o"}).invoke(letter)
    
    return response


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
    

def verfiy_language(letter_content: str):
    promt_text = f"""
        # Original Letter:
        {letter_content}
        
        
       What is the language of the Original Letter?
        
        answer only in format below:
        
        #Format 
       English
    
    """

    prompt = PromptTemplate.from_template(promt_text)

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
        response = chain.invoke(letter_content)

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