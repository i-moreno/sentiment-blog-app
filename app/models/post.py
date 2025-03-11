from pydantic import BaseModel, Field
from typing import Optional


class BlogPost(BaseModel):
    post_id: Optional[str] = None
    title: str
    content: str
    archived: Optional[bool] = False

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
