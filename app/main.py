from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .startup import run_startup_tasks
from .routes import signup, users, authentication, admin

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials =True,
    allow_headers = ["*"],
    allow_methods= ["*"]
    )

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