import uvicorn
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from fastapi.params import Body
from models import Feature, Post


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: float = None

def find_post(id):
    for post in my_post:
        if post['id'] == id:
            return post

my_post = [{'title': "hello world", 'content': 'many people are starting their coding journey by write Hello World program', 'id': 1},
           {'title': 'AI Change industry', 'content': 'due to AI involvment some jobs go down', 'id': 2}]




@app.get("/")
def read_root():
    return {"message": "FastAPI is running on a custom port"}


@app.get("/posts")
def get_post():
    return {'message': my_post,}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    new_post = post.dict()
    new_post['id'] = len(my_post) + 1
    my_post.append(new_post)
    return {'Message': new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return {'message': post}



if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=9000, reload=True)