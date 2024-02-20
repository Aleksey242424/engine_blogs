from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,scoped_session,sessionmaker
from app import login
import enum


engine = create_engine('postgresql+psycopg2://postgres:123@localhost:5432/db_engine_blogs')

db_session = scoped_session(sessionmaker(bind=engine,autoflush=False,autocommit=False,expire_on_commit=False))

Base = declarative_base()

class LikesDislikesEnum(enum.Enum):
    off = 0
    on = 0


@login.user_loader
def get_user(user_id):
    from app.system_db.models import Users
    return Users.query.get(user_id)