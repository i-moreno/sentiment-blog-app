from fastapi import FastAPI, HTTPException, Query
from mangum import Mangum
from typing import Optional
import boto3

from app.models.post import BlogPost, PostUpdate
from app.repo.post import BlogRepository

app = FastAPI(title="Blog API")

dynamo = boto3.resource('dynamodb')
table = dynamo.Table('BlogAppTable')

blog_repo = BlogRepository()


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


handler = Mangum(app)
