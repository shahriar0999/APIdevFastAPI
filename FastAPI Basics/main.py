import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.params import Body
from models import Feature, Post


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: float = None

my_post = [{'title': "hello world", 'content': 'many people are starting their coding journey by write Hello World program', 'id': 1},
           {'title': 'AI Change industry', 'content': 'due to AI involvment some jobs go down', 'id': 2}]




@app.get("/")
def read_root():
    return {"message": "FastAPI is running on a custom port"}


@app.get("/posts")
def get_post():
    return {'message': my_post,}


@app.post("/posts")
def createPost(post: Post):
    new_post = post.dict()
    new_post['id'] = len(my_post) + 1
    my_post.append(new_post)
    return {'Message': new_post}



@app.post("/createpost")
def create_post(payload : dict = Body(...)):
    print(payload)
    return {"new_post": f" title {payload['text']} content {payload['content']}"}



if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=9000, reload=True)