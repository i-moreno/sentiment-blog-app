from sqlalchemy import Column, Integer, ForeignKey, Text
from app.db.database import Base


class Sentiment(Base):
    __tablename__ = "sentiments"
    sentiment_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), index=True)
    brief = Column(Text)
    sentiment = Column(Text)
