from fastapi import FastAPI
# from .startup import run_startup_tasks
from .routes import signup, users, authentication, admin

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
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(admin.router)