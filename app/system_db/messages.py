from app.system_db import db_session
from datetime import datetime

class Messages:
    @staticmethod
    def add(message,user_id,date_send=datetime.utcnow()):
        from app.system_db.models import Messages
        with db_session() as session:
            session.add(Messages(message=message,user_id=user_id,date_send=date_send))
            session.commit()

    @staticmethod
    def get_all():
        from app.system_db.models import Messages
        from app.system_db.models import Users
        with db_session() as session:
            messages = session.query(Messages,Users.avatar,Users.username).join(Users,Messages.user_id == Users.user_id).order_by(Messages.message_id.desc()).all()
            return messages
