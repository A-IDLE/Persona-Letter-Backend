from app.services.model import load_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

def image_questions(letter):

    prompt_text = """
        You are an AI assistant tasked with using a given format to find keywords for a scene that is associated with a given context.
        Please answer in format only and only English, excluding other content. Find at least 3 keywords and no more than 10 keywords. Keywords never include a person's name.
        #question:
        {question}
        
        #example answer format:
        keyword1, keyword2, keyword3, keyword4, keyword5
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