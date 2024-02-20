from app.system_db import db_session,engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text,and_

class Chats:
    @staticmethod
    def add(first_user_id,second_user_id):
        from app.system_db.chats import Chats
        if Chats.check_duplicate(first_user_id,second_user_id):
            return 
        from app.system_db.models import Chats
        with db_session() as session:
            try:
                session.add(Chats(first_user_id=first_user_id,second_user_id=second_user_id))
                session.commit()
            except IntegrityError:
                return
            
    @staticmethod
    def check_duplicate(first_user_id,second_user_id):
        from app.system_db.models import Chats
        with db_session() as session:
            duplicate = session.query(Chats).filter(and_(Chats.first_user_id == second_user_id,Chats.second_user_id == first_user_id)).scalar()
            return duplicate
            
    @staticmethod
    def get_chat_id(first_user_id,second_user_id):
        with db_session() as session:
            chat_id_query = text(f"""
            SELECT chat_id FROM chats WHERE 
            (first_user_id = :first_user_id AND second_user_id = :second_user_id)
            OR 
            (first_user_id = :second_user_id AND second_user_id = :first_user_id)
            """)
            chat_id = session.execute(chat_id_query,{'first_user_id':first_user_id,'second_user_id':second_user_id}).scalar()
            return chat_id
            
    @staticmethod
    def get(user_id):
        with db_session() as session:
            chats = text("""
        SELECT chats.chat_id,chats.first_user_id,
        chats.second_user_id,users.username,users.avatar FROM chats JOIN users
        ON (chats.second_user_id = users.user_id AND users.user_id <> :user_id) 
        OR (chats.first_user_id = users.user_id AND users.user_id <> :user_id)
        WHERE chats.first_user_id = :user_id OR chats.second_user_id = :user_id
            """)
            chats = session.execute(chats,{'user_id':user_id}).all()
            return chats