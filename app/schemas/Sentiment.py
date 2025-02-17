from pydantic import BaseModel


class SentimentBase(BaseModel):
    sentiment: str
    brief: str


class SentimentCreate(SentimentBase):
    pass


class Sentiment(SentimentBase):
    post_id: int
