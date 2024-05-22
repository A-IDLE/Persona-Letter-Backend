from app.models.database import SessionLocal
from app.query.letter import Letter
from app.query.character import Character  

def get_user_inbox(user_id: int, character_id: int):
    try:
        with SessionLocal() as session:  
            # Letter 테이블과 Character 테이블을 조인하고 필요한 정보를 선택합니다.
            inbox_letters_with_characters = session.query(
                Letter, Character.character_name
            ).join(
                Character, Letter.character_id == Character.character_id
            ).filter(
                Letter.user_id == user_id, 
                Letter.character_id == character_id,  # 클릭한 캐릭터 아이디와 일치하는 메일만 가져옵니다.
                Letter.reception_status == "receiving"
            ).all()

            # 결과를 딕셔너리 형태로 포맷하여 리스트에 추가합니다.
            result = []
            for letter, character_name in inbox_letters_with_characters:
                letter_info = {
                    "letter_id": letter.letter_id,
                    "character_name": character_name,
                    "letter_content": letter.letter_content,
                    "letter_image_status": 0,
                    "read_status": letter.read_status,
                    "created_time": letter.created_time,
                    # 추가적으로 필요한 Letter 필드를 여기에 포함시킬 수 있습니다.
                }
                result.append(letter_info)

            return result
    except Exception as e:
        print("삐빅에러",e)  # 오류가 발생하면 오류 메시지를 출력합니다.
        return None


def get_user_outbox(user_id: int, character_id: int):
    try:
         with SessionLocal() as session:  
            # Letter 테이블과 Character 테이블을 조인하고 필요한 정보를 선택합니다.
            outbox_letters_with_characters = session.query(
                Letter, Character.character_name
            ).join(
                Character, Letter.character_id == Character.character_id
            ).filter(
                Letter.user_id == user_id, 
                Letter.character_id == character_id,  # 클릭한 캐릭터 아이디와 일치하는 메일만 가져옵니다.
                Letter.reception_status == "sending"
            ).all()

            # 결과를 딕셔너리 형태로 포맷하여 리스트에 추가합니다.
            result = []
            for letter, character_name in outbox_letters_with_characters:
                letter_info = {
                    "letter_id": letter.letter_id,
                    "character_name": character_name,
                    "letter_content": letter.letter_content,
                    "letter_image_status": 0,
                    "read_status": letter.read_status,
                    "created_time": letter.created_time,
                    # 추가적으로 필요한 Letter 필드를 여기에 포함시킬 수 있습니다.
                }
                result.append(letter_info)

            return result
    except Exception as e:
        print(e)  # 오류가 발생하면 오류 메시지를 출력합니다.
        return None
