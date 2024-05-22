from app.models.database import SessionLocal
from app.models.models import Relationship




def create_relationship(relationship: Relationship):
    try:
        with SessionLocal() as session:
            session.add(relationship)
            session.commit()
            return relationship
    except Exception as e:
        return f"Error saving the relationship: {str(e)}"

def get_relationship_by_id(relationship_id: int):
    try:
        with SessionLocal() as session:
            relationship = session.query(Relationship).filter(Relationship.relationship_id == relationship_id).first()
            return relationship
    except Exception as e:
        return f"Error getting the relationship: {str(e)}"

def get_relationships_by_user(user_id: int):
    try:
        with SessionLocal() as session:
            relationships = session.query(Relationship).filter(Relationship.user_id == user_id).all()
            return relationships
    except Exception as e:
        return f"Error getting relationships for user: {str(e)}"

def get_relationships_by_character(character_id: int):
    try:
        with SessionLocal() as session:
            relationships = session.query(Relationship).filter(Relationship.character_id == character_id).all()
            return relationships
    except Exception as e:
        return f"Error getting relationships for character: {str(e)}"

def update_relationship_active_status(relationship_id: int, active_status: bool):
    try:
        with SessionLocal() as session:
            relationship = session.query(Relationship).filter(Relationship.relationship_id == relationship_id).first()
            if relationship:
                relationship.active_status = active_status
                session.commit()
                return "Relationship active status updated successfully."
            else:
                return "Relationship not found."
    except Exception as e:
        return f"Error updating relationship active status: {str(e)}"

def delete_relationship_by_id(relationship_id: int):
    try:
        with SessionLocal() as session:
            relationship = session.query(Relationship).filter(Relationship.relationship_id == relationship_id).first()
            if relationship:
                session.delete(relationship)
                session.commit()
                return "Relationship deleted successfully."
            else:
                return "Relationship not found."
    except Exception as e:
        return f"Error deleting the relationship: {str(e)}"