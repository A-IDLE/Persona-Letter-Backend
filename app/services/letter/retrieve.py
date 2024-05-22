import json
from services.retriever import get_pinecone_retriever
from .generate import generate_questions

def retrieve_letter(questions, user_id, character_id):
    letters = get_pinecone_retriever(user_id, character_id, questions)
    return letters

def retrieve_through_letter(letter_content, user_id, character_id):
    questions = generate_questions(letter_content)
    questions = json.loads(questions)
    related_letters = retrieve_letter(questions, user_id, character_id)
    return related_letters