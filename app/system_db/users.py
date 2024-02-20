from app.system_db import db_session
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.exc import IntegrityError

class Users:
    @staticmethod
    def add(username:str,password:str,email:str):
        from app.system_db.models import Users
        with db_session() as session:
            try:
                session.add(Users(username=username,hash_password=generate_password_hash(password),email=email))
                session.commit()
                return True
            except IntegrityError:
                return
            
    @staticmethod
    def get_instance(username,password):
        from app.system_db.models import Users
        with db_session() as session:
            try:
                user = session.query(Users).filter(Users.username==username,
                                            check_password_hash(
                                                session.query(Users.hash_password).filter(Users.username==username).scalar(),
                                                password
                                                ) == True 
                                            ).scalar()
                return user
            except AttributeError:
                return
            
    @staticmethod
    def get_user_id_by_email(email):
        from app.system_db.models import Users
        with db_session() as session:
            user_id = session.query(Users.user_id).filter_by(email=email).scalar()
            return user_id
        

    @staticmethod
    def update_password(user_id,password):
        from app.system_db.models import Users
        with db_session() as session:
            user = session.query(Users).get(user_id)
            user.hash_password = generate_password_hash(password)
            session.commit()

    @staticmethod
    def get_data(username):
        from app.system_db.models import Users
        with db_session() as session:
            user = session.query(Users).filter_by(username=username).scalar()
            return user
        
    @staticmethod
    def update_avatar(user_id,avatar):
        from app.system_db.models import Users
        with db_session() as session:
            user = session.query(Users).get(user_id)
            user.avatar = avatar
            session.commit()
    @staticmethod
    def get_id(username):
        from app.system_db.models import Users
        with db_session() as session:
            user_id = session.query(Users.user_id).filter_by(username=username).scalar()
            return user_id