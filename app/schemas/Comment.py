from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    comment_id: int
    post_id: int

    class Config:
        from_attributes = True
