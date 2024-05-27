import json
from requests import Session
from .generate import generate_questions
from app.services.retriever import get_pinecone_retriever, get_pinecone_retriever_test, PineconeRetriever
from typing import List, Dict
from app.services.letter.generate import refining_retrieved_info

def retrieve_letter(
    user_id:int, 
    character_id:int, 
    questions:List[Dict],
    top_k:int =5
):
    
    retriever = PineconeRetriever(top_k=top_k)
    letters = retriever.retrieve(user_id, character_id, questions)
    
    # letters = get_pinecone_retriever(user_id, character_id, questions)
    
    return letters

def retrieve_through_letter(letter_content, user_id, character_id):
    generated_questions = generate_questions(letter_content)
    questions = json.loads(generated_questions)
    related_letters = retrieve_letter(user_id, character_id, questions)
    return related_letters

def retrieve_letter_test(questions, user_id, character_id, top_k):
    letters = get_pinecone_retriever_test(user_id, character_id, questions, top_k)
    return letters


def retrieve_through_letter_update(generated_questions:str, user_id:int, character_id:int) -> str:
    """_summary_

    Args:
        letter_content (str): _description_
        user_id (int): _description_
        character_id (int): _description_

    Returns:
        str: _description_
    """
    
    # convert generated questions to list
    questions = json.loads(generated_questions)
    
    # Initialize retriever
    retriever = PineconeRetriever(top_k=3)
    
    # retrieve related information
    retrieved_info_list = retriever.retrieve(user_id, character_id, questions)
    retrieved_info_str = "".join(f"- {retrieved_info}\n"for retrieved_info in retrieved_info_list)
    
    # refine retrieved information with generated questions and retrieved information
    refined_retrieved_info = refining_retrieved_info(generated_questions, retrieved_info_str)

    return refined_retrieved_info

