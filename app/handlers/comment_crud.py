from sqlalchemy.orm import Session
from app.models.Comment import Comment
from app.schemas.Comment import CommentCreate


def create_comment(db: Session, post_id: int, comment: CommentCreate):
    db_comment = Comment(post_id=post_id, content=comment.content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_post_comments(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
