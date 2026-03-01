from fastapi import FastAPI
# from .startup import run_startup_tasks
from .routes import signup

app = FastAPI()

@app.get("/")
def root():
    {
        "message":"Hey there welcome to TaskReady API"
    }

# @app.on_event("startup")
# def startup_event():
#     print("🚀 FastAPI startup event triggered")
#     run_startup_tasks()


app.include_router(signup.router)