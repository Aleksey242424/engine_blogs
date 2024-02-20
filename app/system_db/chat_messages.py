from app.system_db import db_session
from datetime import datetime
from sqlalchemy import or_

class ChatsMessages:
    @staticmethod
    def add(chat_id,sender_id,recipient_id,message):
        from app.system_db.models import ChatMessages
        with db_session() as session:
            session.add(ChatMessages(chat_id=chat_id,sender_id=sender_id,
                                     recipient_id=recipient_id,
                                     message=message,date_send=datetime.utcnow()))
            session.commit()

    @staticmethod
    def get(chat_id):
        from app.system_db.models import ChatMessages,Users
        with db_session() as session:
            messages = session.query(ChatMessages.message,ChatMessages.date_send,Users.username).join(Users,ChatMessages.sender_id == Users.user_id).filter(ChatMessages.chat_id==chat_id).order_by(ChatMessages.message_id.desc()).all()
            return messages
        
