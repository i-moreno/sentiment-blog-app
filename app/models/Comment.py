from sqlalchemy import Column, Integer, ForeignKey, Text
from app.db.database import Base


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    content = Column(Text)
