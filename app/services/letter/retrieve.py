import json
from requests import Session
from .generate import generate_questions
from app.services.retriever import get_pinecone_retriever, get_pinecone_retriever_test, PineconeRetriever

def retrieve_letter(user_id, character_id, questions):
    
    retriever = PineconeRetriever()
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


def retrieve_through_letter_update(letter_content:str, user_id:int, character_id:int) -> str:
    """_summary_

    Args:
        letter_content (str): _description_
        user_id (int): _description_
        character_id (int): _description_

    Returns:
        str: str of list of related letters
    """
    
    generated_questions = generate_questions(letter_content)
    questions = json.loads(generated_questions)
    retriever = PineconeRetriever()
    related_letters = retriever.retrieve(user_id, character_id, questions)
    related_letters_str = "".join(f"- {related_letter}\n"for related_letter in related_letters)

    return related_letters_str

