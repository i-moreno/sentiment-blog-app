from sqlalchemy.orm import Session
from app.models.Sentiment import Sentiment
from app.schemas.Sentiment import SentimentCreate


def create_sentiment(db: Session, post_id: int, sentiment: SentimentCreate):
    db_sentiment = Sentiment(
        post_id=post_id, sentiment=sentiment.sentiment, brief=sentiment.brief)
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    return db_sentiment
