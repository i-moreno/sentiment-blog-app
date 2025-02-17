from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base


class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    image_url = Column(String, nullable=True)
    sentiment_id = Column(Text)
