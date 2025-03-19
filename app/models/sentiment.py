from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Sentiment(BaseModel):
    sentiment_id: str
    sentiment: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SentimentUpdate(BaseModel):
    sentiment: str
    last_updated_at: Optional[datetime] = None
