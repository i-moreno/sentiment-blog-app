from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import SessionLocal, engine, Base
from app.handlers import post_crud, comment_crud
from app.schemas.Post import BlogPost, BlogPostCreate
from app.schemas.Comment import Comment, CommentCreate

import app.models

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")


# Dependency to get a database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"status": "ok"}


# Endpoint to retrieve all blog posts
@app.get("/posts", response_model=List[BlogPost])
def list_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = post_crud.get_blog_posts(db, skip=skip, limit=limit)
    return posts


# Endpoint to create a new blog post
@app.post("/posts", response_model=BlogPost)
def create_post(post: BlogPostCreate, db: Session = Depends(get_db)):
    return post_crud.create_blog_post(db, post)


#  Endpoint to retrieve a single blog post by ID
@app.get("/posts/{post_id}", response_model=BlogPost)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = post_crud.get_blog_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


# Endpoint to add a comment to a specific blog post
@app.post("/posts/{post_id}/comments", response_model=Comment)
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    post = post_crud.get_blog_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return comment_crud.create_comment(db, post_id, comment)


# Endpoint to get comments for an specific post
@app.get("/posts/{post_id}/comments", response_model=List[Comment])
def get_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return comment_crud.get_post_comments(db, post_id, skip=skip, limit=limit)
