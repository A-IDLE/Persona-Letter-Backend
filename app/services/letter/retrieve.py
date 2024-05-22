import json
from .generate import generate_questions
from app.services.retriever import get_pinecone_retriever, get_pinecone_retriever_test

def retrieve_letter(questions, user_id, character_id):
    letters = get_pinecone_retriever(user_id, character_id, questions)
    return letters

def retrieve_through_letter(letter_content, user_id, character_id):
    questions = generate_questions(letter_content)
    questions = json.loads(questions)
    related_letters = retrieve_letter(questions, user_id, character_id)
    return related_letters

def retrieve_letter_test(questions, user_id, character_id, top_k):
    letters = get_pinecone_retriever_test(user_id, character_id, questions, top_k)
    return letters

