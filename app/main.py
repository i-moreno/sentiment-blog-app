from fastapi import FastAPI
from mangum import Mangum

import boto3

app = FastAPI(title="Blog API")

dynamo = boto3.resource('dynamodb')
table = dynamo.Table('BlogAppTable')


@app.get("/")
def read_root():
    return {"status": "ok"}


# # Endpoint to create a new blog post
@app.post("/posts")
def create_post(post: dict):
    table.put_item(Item={'postId': post.post_id, **post})
    return {'message': 'Post created successfully'}


handler = Mangum(app)
