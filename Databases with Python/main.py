import time
import uvicorn
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor



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

def find_post_index(id):
    for i, post in enumerate(my_post):
        if post['id'] == id:
            return i

# connect with database
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='1212759382',
                          cursor_factory=RealDictCursor)
        cursor =conn.cursor()
        print("Successfully Connected to PostgreSQL")
        break

    except Exception as error :
        print("could not connect to PostgreSQL")
        print("error: ", error)
        time.sleep(2)

my_post = [{'title': "hello world", 'content': 'many people are starting their coding journey by write Hello World program', 'id': 1},
           {'title': 'AI Change industry', 'content': 'due to AI involvment some jobs go down', 'id': 2}]




@app.get("/")
def read_root():
    return {"message": "FastAPI is running on a custom port"}


@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts =  cursor.fetchall()
    return {'message': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'Message': new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return {'message': post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (id,))
    conn.commit()
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    return {'data': updated_post}


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=9000, reload=True)