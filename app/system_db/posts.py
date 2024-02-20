from app.system_db import db_session
from sqlalchemy import func


class Posts:
    @staticmethod
    def add(title,body,user_id):
        from app.system_db.models import Posts
        from app.system_db.elastic import add_post
        with db_session() as session:
            session.add(Posts(title=title,body=body,user_id=user_id))
            session.commit()
        from app.system_db.posts import Posts
        last_id = Posts.get_last_id()
        if last_id:
            add_post('index_post',title,body,last_id[0])
        else:
            add_post('index_post',title,body,1)

    @staticmethod
    def get(post_id):
        from app.system_db.models import Posts
        with db_session() as session:
            post = session.query(Posts).get(post_id)
            return post
        
    @staticmethod
    def get_last_id():
        from app.system_db.models import Posts
        with db_session() as session:
            last_id = session.query(Posts.post_id).order_by(Posts.post_id.desc()).first()
            return last_id
        
    @staticmethod
    def get_user_posts(username,page):
        from app.system_db.models import Posts,Users
        with db_session() as session:
            posts = session.query(Posts).filter(
                Posts.user_id == session.query(Users.user_id)
                .filter_by(username=username).scalar()
                ).offset((page-1)*3).limit(3).all()
            return posts
        
    @staticmethod
    def get_post(post_id):
        from app.system_db.models import Posts
        with db_session() as session:
            post = session.query(Posts).filter_by(post_id=post_id).scalar()
            return post
        
    @staticmethod
    def get_count_my_post_group(username):
        from app.system_db.models import Posts,Users
        with db_session() as session:
            count = session.query(Posts).filter(
                Posts.user_id == session.query(Users.user_id)
                .filter_by(username=username).scalar()
                ).count()
            
            count_group = int(-1*(count/3)//1*-1)
            return count_group
        
    @staticmethod
    def get_posts(page):
        from app.system_db.models import Posts,LikesDislikes
        with db_session() as session:
            posts = session.query(Posts).order_by(Posts.post_id.desc()).offset((page-1)*3).limit(3).all()
            return posts
        
    @staticmethod
    def get_recom_posts(page):
        from app.system_db.models import Posts,LikesDislikes
        with db_session() as session:
            posts = session.query(Posts).join(LikesDislikes,Posts.post_id==LikesDislikes.post_id).filter(LikesDislikes.likes == 'True').group_by(Posts.post_id).order_by(func.count(LikesDislikes.likes).desc()).offset((page-1)*3).limit(3).all()
            return posts
    
    



