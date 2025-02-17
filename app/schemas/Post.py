from pydantic import BaseModel
from typing import Optional


class BlogPostBase(BaseModel):
    title: str
    content: str
    imageUrl: Optional[str] = None


class BlogPostCreate(BlogPostBase):
    pass


class BlogPost(BlogPostBase):
    post_id: int
    sentiment: Optional[str] = None

    class Config:
        from_attributes = True
