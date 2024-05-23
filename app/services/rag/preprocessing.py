import nltk
from nltk.tokenize import sent_tokenize
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings
from langchain_core.documents.base import Document
from langchain.storage import LocalFileStore
from openai import OpenAI
from openai import OpenAIError
import os
from app.utils.utils import load_pdf, load_txt, identify_path
from app.services.vector_database import load_vector_db, pinecone_upsert
from app.models.models import Letter




nltk.download('punkt')

# Function to split text into chunks
def split_into_chunks(text, max_chunk_size=512):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []

    current_length = 0
    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

import spacy
from transformers import pipeline
from nltk.corpus import stopwords


# Load models
# Load models
nlp = spacy.load("en_core_web_sm")
coref = pipeline("coreference-resolution")
nltk.download('stopwords')



# Function for advanced preprocessing
def advanced_preprocessing(text):
    # Coreference resolution
    coref_result = coref(text)
    resolved_text = coref_result[0]['resolved']

    # NER and POS tagging
    doc = nlp(resolved_text)
    processed_text = []
    for token in doc:
        if token.ent_type_:
            processed_text.append(f"{token.ent_type_}_{token.text}_{token.pos_}")
        else:
            processed_text.append(f"{token.text}_{token.pos_}")

    # Join processed text
    processed_text = ' '.join(processed_text)

    # Lemmatization
    lemmatized_text = []
    for token in doc:
        lemmatized_text.append(token.lemma_)
    lemmatized_text = ' '.join(lemmatized_text)

    # Remove stop words carefully
    stop_words = set(stopwords.words('english'))
    words = lemmatized_text.split()
    final_text = ' '.join([word for word in words if word not in stop_words])

    return final_text



def embed_letter_pinecone(letter: Letter):
    # Initialize the text splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0, length_function=len, separators=["\n", ". "])

    # Split the document
    split_texts = splitter.split_text(letter.letter_content)
    print(f"\n\n embed_letter_pinecone SPLIT DOCS total documents: {len(split_texts)}\n\n")

    # Convert split documents to vectors
    vector_data = []
    namespace = f"{letter.user_id}_{letter.character_id}"
    embeddings = text_to_vector(split_texts)  # Get embeddings for all texts at once
    print(f"text_to_vector function completed for {len(embeddings['data'])} documents.")

    for idx, (text, vector) in enumerate(zip(split_texts, embeddings['data'])):
        vector_entry = {
            "id": f"{letter.letter_id}_{idx}",  # Creating a composite ID
            "values": vector['embedding'],
            "metadata": {
                "letter_id": letter.letter_id,
                "character_id": letter.character_id,
                "user_id": letter.user_id,
                "reception_status": letter.reception_status,
                "created_time": letter.created_time,
                "text": text,
            },
        }
        vector_data.append(vector_entry)

    # upsert vector data into the Pinecone index
    response = pinecone_upsert(vector_data, namespace)

    return response

# Example function to convert text to vector
def text_to_vector(texts):
    try:
        load_dotenv()
        model = os.getenv('EMBEDDING_MODEL')
        client = OpenAI()
        embeddings = client.embeddings.create(
            model=model,
            input=texts,
            encoding_format="float"
        )
        embeddings = embeddings.to_dict()
        print(f"Text to vector function completed for {len(embeddings['data'])} documents.")
        return embeddings
    except OpenAIError as e:
        print(f"An error occurred while generating embeddings: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None