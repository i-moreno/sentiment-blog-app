from typing import List
from sqlalchemy.orm import Session
from app.models.Post import Post
from app.schemas.Post import BlogPostCreate


def get_blog_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).offset(skip).limit(limit).all()


def get_blog_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.post_id == post_id).first()


def create_blog_post(db: Session, post: BlogPostCreate):
    db_post = Post(title=post.title, content=post.content,
                   image_url=post.imageUrl)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
