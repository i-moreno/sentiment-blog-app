from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Comment(BaseModel):
    comment_id: Optional[str] = None
    content: str
    archived: Optional[bool] = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    content: str
    last_updated_at: Optional[datetime] = None
