from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from .base import Base

class Character(Base):
    __tablename__ = 'tbl_character'

    character_id = Column(Integer, primary_key=True, autoincrement=True)
    character_name = Column(String(255), nullable=False)
    biography = Column(Text)
    physical_description = Column(Text)
    personality_and_trait = Column(Text)
    magical_abilities_and_skills = Column(Text)
    possessions = Column(Text)
    relationships = Column(Text)
    etymology = Column(Text)
    examples_tone_of_voice = Column(Text)
    character_image_url = Column(String(2048))
    series = Column(String(1024))
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, onupdate=func.now())
    
class Letter(Base):
    __tablename__ = 'tbl_letter'
    
    letter_id = Column(Integer, primary_key=True, autoincrement=True)
    # character_id = Column(Integer, ForeignKey('tbl_character.character_id'))
    character_id = Column(Integer)
    # user_id = Column(Integer, ForeignKey('tbl_user.user_id'))
    user_id = Column(Integer)
    reception_status = Column(String(30))
    letter_content = Column(Text)
    letter_image_status = Column(Boolean, default=False)
    read_status = Column(Boolean, default=False)
    created_time = Column(DateTime, server_default=func.now())
    
    
class User(Base):
    __tablename__ = 'tbl_user'  

    user_id = Column(Integer, primary_key=True, autoincrement=True)  # Simplify the name to 'id'
    email = Column(String(100), nullable=False, unique=True)  # Emails should be unique and not nullable
    password = Column(String(100), nullable=True)  # Passwords should not be nullable
    user_name = Column(String(100), nullable=True)  # Changed from Text to String if not expected to exceed typical varchar limits
    user_nickname = Column(String(100), nullable=True)
    created_time = Column(DateTime(timezone=True), server_default=func.now())  # Use DateTime type and set default as the current time
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())  # Update the timestamp whenever the record is updated
    sso_type = Column(String(100), nullable=True) 
    
    
class Relationship(Base):
    __tablename__ = 'tbl_relationship'
    
    relationship_id = Column(Integer, primary_key=True, autoincrement=True)
    # user_id = Column(Integer, ForeignKey('tbl_user.user_id'), nullable=False)
    user_id = Column(Integer)
    # character_id = Column(Integer, ForeignKey('tbl_character.character_id'), nullable=False)
    character_id = Column(Integer)
    relationship_content = Column(Text, nullable=True)
    active_status = Column(Boolean, default=True)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, onupdate=func.now())
    
class RagTestData(Base):
    __tablename__ = 'tbl_rag_test_data'
    
    rag_test_data_id = Column(Integer, primary_key=True, autoincrement=True)
    created_time = Column(DateTime, server_default=func.now())
    version = Column(String(100))
    changes = Column(Text, nullable=True)
    request_letter_content = Column(Text)
    response_letter_content = Column(Text)
    chunk_size = Column(Integer)
    chunk_overlap = Column(Integer)
    top_k = Column(Integer)
    filter = Column(Text, nullable=True)
    basic_character_prompt = Column(Text)
    generate_questions_prompts = Column(Text)
    generated_questions = Column(JSON)
    retrieved_info = Column(JSON)
    refining_retrieved_info_prompt = Column(Text)
    refined_info = Column(Text)
    notes = Column(Text, nullable=True)
    updated_time = Column(DateTime, onupdate=func.now(), nullable=True)
    total_words = Column(Integer, nullable=True)