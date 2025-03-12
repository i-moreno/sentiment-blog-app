from pydantic import BaseModel
from typing import Optional


class Comment(BaseModel):
    comment_id: Optional[str] = None
    content: str
    archived: Optional[bool] = False

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    content: str
