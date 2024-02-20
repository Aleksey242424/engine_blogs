from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey,PrimaryKeyConstraint,ForeignKeyConstraint,UniqueConstraint
from app.system_db import Base,db_session,engine
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy.types import Enum,Integer
from sqlalchemy import text

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

class LikesDislikes(Base):
    __tablename__ = 'likes_dislikes'
    likes = Column(Enum('True','False',name='state'),default=False)
    dislikes = Column(Enum('True','False',name='state'),default=False)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.user_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    post_id:Mapped[int] = mapped_column(ForeignKey('posts.post_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)

    __table_args__ = (PrimaryKeyConstraint(user_id,post_id,name='pk_user_post'),)

class Chats(Base):
    __tablename__ = 'chats'
    chat_id:Mapped[int] = mapped_column(primary_key=True)
    first_user_id:Mapped[int] = mapped_column(ForeignKey('users.user_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    second_user_id:Mapped[int] = mapped_column(ForeignKey('users.user_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    __table_args__ = (UniqueConstraint(first_user_id,second_user_id,name='compose_id'),)

class ChatMessages(Base):
    __tablename__ = 'chat_messages'
    message_id:Mapped[int] = mapped_column(primary_key=True)
    chat_id:Mapped[int] = mapped_column(ForeignKey('chats.chat_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    sender_id:Mapped[int] = mapped_column(ForeignKey('users.user_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    recipient_id:Mapped[int] = mapped_column(ForeignKey('users.user_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    message:Mapped[str] = mapped_column(nullable=False)
    date_send:Mapped[datetime] = mapped_column(nullable=False)

Base.metadata.create_all(engine)