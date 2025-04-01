import uvicorn
from fastapi import FastAPI
import routers.post as post
import routers.user as user
import models
from database import engine


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "FastAPI is running on a custom port"}


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=9002, reload=True)