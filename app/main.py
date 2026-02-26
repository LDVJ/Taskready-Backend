from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    {
        "message":"Hey there welcome to TaskReady API"
    }