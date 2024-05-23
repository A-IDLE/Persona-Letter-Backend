import nltk
from nltk.tokenize import sent_tokenize
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


# Example long letter
long_letter = """
Dear John,
I hope this letter finds you well. I wanted to update you on the project. The initial phase is complete, and we are moving to the next stage. There are a few challenges we are facing, such as coordinating with the different departments to ensure that everyone is on the same page and adhering to the timelines. Additionally, we have encountered some technical issues with the new software integration, which our IT team is currently addressing.

Despite these challenges, the team remains optimistic and committed to overcoming any obstacles. We are working diligently to find solutions and ensure the project's success. I will continue to keep you informed of our progress and any significant developments.

Thank you for your continued support and understanding.

Best regards,

James
"""

chunks = split_into_chunks(long_letter)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}: {chunk}\n")



import spacy
from transformers import pipeline
from nltk.corpus import stopwords

# Load models
nlp = spacy.load("en_core_web_sm")
coref = pipeline("spanbert_large")
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

# Apply advanced preprocessing to each chunk
processed_chunks = [advanced_preprocessing(chunk) for chunk in chunks]
for i, processed_chunk in enumerate(processed_chunks):
    print(f"Processed Chunk {i + 1}: {processed_chunk}\n")
