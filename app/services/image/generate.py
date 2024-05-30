from app.services.model import load_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

def image_questions(letter):

    prompt_text = """
        You are an AI assistant tasked with using a given format to find keywords to visually depict a scene described by a given context.
        Extract only keywords that describe actions, background, attire, and overall appearance of the writer of the {question}.
        Do not include any keywords that represent abstract concepts such as 'love', 'knowledge', 'bond', 'passion', 'empathy', and so on. 
        If there are no keywords that can visually describe the scene, include a single random word representing daily life activity.
        Please answer in format only excluding other content, and only in English. 
        Find at least 3 keywords and no more than 10 keywords. 
        Keywords never include a person's name.
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