from fastapi import FastAPI, HTTPException, Query
from mangum import Mangum
from typing import Optional

from app.models.post import BlogPost, PostUpdate
from app.models.comment import Comment, CommentUpdate
from app.models.sentiment import Sentiment, SentimentUpdate
from app.repo.post import BlogRepository
from app.repo.comment import CommentRepository
from app.repo.sentiment import SentimentRepository

app = FastAPI(title="Blog API")

blog_repo = BlogRepository()
comment_repo = CommentRepository()
sentiment_repo = SentimentRepository()


@app.get("/")
def read_root():
    return {"status": "ok"}


# LIST posts
@app.get("/posts")
def get_posts(
    limit: int = 10,
    last_evaluated_pk: Optional[str] = None,
    last_evaluated_gsi: Optional[str] = None,
    sort_order: str = Query('DESC', regex="^(ASC|DESC)$")
):
    try:
        posts, next_key = blog_repo.read_posts(
            limit=limit,
            last_evaluated_pk=last_evaluated_pk,
            last_evaluated_gsi=last_evaluated_gsi,
            sort_order=sort_order
        )
        return {
            "posts": posts,
            "next_key": next_key
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# CREATE post
@app.post("/post")
def create_post(post: BlogPost):
    try:
        created_post = blog_repo.create_post(post)
        return {"message": 'Post created successfully', "post": created_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update post
@app.patch("/post/{post_id}")
def update_post(post_id: str, updates: PostUpdate):
    try:
        updated_post = blog_repo.update_post(post_id=post_id, post=updates)
        return {"message": "Post updated correctly", "post": updated_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/post/{post_id}")
def delete_post(post_id: str):
    try:
        deleted_post = blog_repo.delete_post(post_id=post_id)
        return {"message": "Post deleted correctly", "post": deleted_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/post/restore/{post_id}")
def restore_post(post_id: str):
    try:
        restored_post = blog_repo.restore_post(post_id=post_id)
        return {"message": 'Post restored successfully', "post": restored_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create comment
@app.post("/comment/{post_id}")
def create_comment(post_id: str, comment: Comment):
    try:
        comment_created = comment_repo.create_comment(
            post_id=post_id, comment=comment)
        return {"message": 'Comment created correctly', "comment": comment_created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# List Comments
@app.get("/comment/{post_id}")
def get_comments(post_id: str, limit: int = 5, last_evaluated_pk: str = None, last_evaluated_sk: str = None):
    try:
        comments, next_key = comment_repo.get_post_comments(
            post_id=post_id,
            limit=limit,
            last_evaluated_pk=last_evaluated_pk,
            last_evaluated_sk=last_evaluated_sk)
        return {"comments":  comments, "next_key": next_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/comment/{post_id}/{comment_id}")
def update_comment(post_id: str, comment_id: str,  comment: CommentUpdate):
    try:
        updated_comment = comment_repo.update_comment(
            post_id=post_id, comment_id=comment_id, comment=comment)
        return {"message": 'Comment updated successfully', "comment": updated_comment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/comment/{post_id}/{comment_id}")
def delete_comment(post_id: str, comment_id: str):
    try:
        comment_repo.delete_comment(post_id=post_id, comment_id=comment_id)
        return {"message": "Comment deleted correctly"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sentiment/{post_id}")
def create_sentiment(post_id: str, sentiment: Sentiment):
    try:
        sentiment_created = sentiment_repo.create_sentiment(
            post_id=post_id, sentiment=sentiment)
        return {"message": 'Sentiment created successfully', "sentiment": sentiment_created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/comment/{post_id}/{sentiment_id}")
def update_sentiment(post_id: str, sentiment_id: str, sentiment: SentimentUpdate):
    try:
        updated_sentiment = sentiment_repo.update_sentiment(
            post_id=post_id, sentiment_id=sentiment_id, sentiment=sentiment)
        return {"message": 'Sentiment updated successfully', "comment": updated_sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


handler = Mangum(app)
