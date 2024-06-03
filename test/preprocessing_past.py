# import os
# import sys
# sys.path.insert(0, os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '..')))

# from allennlp.predictors.predictor import Predictor
# import spacy
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize
# nltk.download('punkt')
# nltk.download('stopwords')

# # Initialize spaCy model
# nlp = spacy.load("en_core_web_sm")

# # Initialize AllenNLP coreference resolution model
# coref = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")

# # Function to split text into chunks
# def split_into_chunks(text, max_chunk_size=512):
#     sentences = sent_tokenize(text)
#     chunks = []
#     current_chunk = []

#     current_length = 0
#     for sentence in sentences:
#         sentence_length = len(sentence.split())
#         if current_length + sentence_length > max_chunk_size:
#             chunks.append(' '.join(current_chunk))
#             current_chunk = [sentence]
#             current_length = sentence_length
#         else:
#             current_chunk.append(sentence)
#             current_length += sentence_length

#     if current_chunk:
#         chunks.append(' '.join(current_chunk))

#     return chunks

# # Function for advanced preprocessing
# def advanced_preprocessing(text):
#     # Coreference resolution
#     coref_result = coref.predict(document=text)
#     resolved_text = text
#     for cluster in coref_result['clusters']:
#         main_mention = coref_result['document'][cluster[0][0]:cluster[0][1]+1]
#         for mention in cluster[1:]:
#             resolved_text = resolved_text.replace(coref_result['document'][mention[0]:mention[1]+1], main_mention)

#     # NER and POS tagging
#     doc = nlp(resolved_text)
#     processed_text = []
#     for token in doc:
#         if token.ent_type_:
#             processed_text.append(f"{token.ent_type_}_{token.text}_{token.pos_}")
#         else:
#             processed_text.append(f"{token.text}_{token.pos_}")

#     # Join processed text
#     processed_text = ' '.join(processed_text)

#     # Lemmatization
#     lemmatized_text = [token.lemma_ for token in doc]
#     lemmatized_text = ' '.join(lemmatized_text)

#     # Remove stop words carefully
#     stop_words = set(stopwords.words('english'))
#     words = lemmatized_text.split()
#     final_text = ' '.join([word for word in words if word not in stop_words])

#     return final_text

# # Example long letter
# long_letter = """
# Dear John,
# I hope this letter finds you well. I wanted to update you on the project. The initial phase is complete, and we are moving to the next stage. There are a few challenges we are facing, such as coordinating with the different departments to ensure that everyone is on the same page and adhering to the timelines. Additionally, we have encountered some technical issues with the new software integration, which our IT team is currently addressing.

# Despite these challenges, the team remains optimistic and committed to overcoming any obstacles. We are working diligently to find solutions and ensure the project's success. I will continue to keep you informed of our progress and any significant developments.

# Thank you for your continued support and understanding.

# Best regards,

# James
# """

# chunks = split_into_chunks(long_letter)

# # Apply advanced preprocessing to each chunk
# processed_chunks = [advanced_preprocessing(chunk) for chunk in chunks]
# for i, processed_chunk in enumerate(processed_chunks):
#     print(f"Processed Chunk {i + 1}: {processed_chunk}\n")
