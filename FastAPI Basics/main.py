import uvicorn
from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running on a custom port"}



@app.post("/createpost")
def create_post(payload : dict = Body(...)):
    print(payload)
    return {"new_post": f" title {payload['text']} content {payload['content']}"}



if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=9000, reload=True)