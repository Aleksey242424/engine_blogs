from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey
from app.system_db import Base,db_session,engine
from datetime import datetime
from flask_login import UserMixin

class Users(Base,UserMixin):
    __tablename__ = 'users'

    user_id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(unique=True,nullable=False)
    hash_password:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(nullable=False,unique=True)
    avatar:Mapped[str] = mapped_column(default='images/default_avatar.jpg')
    about_me:Mapped[str] = mapped_column(nullable=True)
    last_seen:Mapped[datetime] = mapped_column(default=datetime.utcnow())


    def get_id(self):
        return self.user_id
    
    query = db_session.query_property()


class Messages(Base):
    __tablename__ = 'messages'

    message_id:Mapped[int] = mapped_column(primary_key=True)
    message:Mapped[str] = mapped_column(nullable=False)
    date_send:Mapped[datetime] = mapped_column(nullable=False)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.user_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)

class Posts(Base):
    __tablename__ = 'posts'

    post_id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(nullable=False)
    body:Mapped[str] = mapped_column(nullable=False)
    preview:Mapped[str] = mapped_column(default='default_preview.jpg')
    user_id:Mapped[int] = mapped_column(ForeignKey('users.user_id',ondelete='CASCADE',onupdate='CASCADE'))


Base.metadata.create_all(engine)