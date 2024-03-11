from app.system_db import db_session
from app.system_db.models import Posts
from sqlalchemy import or_



def get_posts(data):
    data = f"%{data}%"
    with db_session() as session:
        posts = session.query(Posts.post_id,Posts.title).filter(or_(Posts.title.like(data),
                                                Posts.body.like(data))).all()
        return posts

