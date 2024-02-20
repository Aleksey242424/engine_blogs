from app.system_db import db_session
from sqlalchemy.exc import IntegrityError

class LikesDislikes:
    

    @staticmethod
    def add(user_id,post_id,like,dislike):
        from app.system_db.models import LikesDislikes
        with db_session() as session:
            try:
                session.add(LikesDislikes(user_id=user_id,post_id=post_id,
                                        likes=like,dislikes=dislike))
                session.commit()
            except IntegrityError:
                from app.system_db.likes_dislikes import LikesDislikes
                session.rollback()
                LikesDislikes.update(user_id,post_id,like,dislike)
            

    @staticmethod
    def update(user_id,post_id,like,dislike):
        with db_session() as session:
            from app.system_db.likes_dislikes import LikesDislikes
            state = LikesDislikes.check_state(user_id=user_id,post_id=post_id)
            from app.system_db.models import LikesDislikes
            if not state or getattr(state,'likes',None) != like or getattr(state,'dislikes',None) != dislike:
                session.query(LikesDislikes).filter_by(user_id = user_id,post_id=post_id).update({'likes':like,'dislikes':dislike})
                session.commit()
            else:
                session.query(LikesDislikes).filter_by(user_id = user_id,post_id=post_id).update({'likes':'False','dislikes':'False'})
                session.commit()

    @staticmethod
    def check_state(user_id,post_id):
        from app.system_db.models import LikesDislikes
        with db_session() as session:
            state = session.query(LikesDislikes).filter_by(user_id=user_id,post_id=post_id).scalar()
            return state
    
    @staticmethod
    def get(post_id):
        from app.system_db.models import LikesDislikes
        with db_session() as session:
            likes = session.query(LikesDislikes).filter_by(post_id=post_id,likes='True').count()
            dislikes = session.query(LikesDislikes).filter_by(post_id=post_id,dislikes='True').count()
            avg_likes = likes-dislikes
            return avg_likes