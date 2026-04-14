from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import auth, projects, messages, profile

app = FastAPI(title="個人履歷網站 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(messages.router)
app.include_router(profile.router)


@app.get("/")
def root():
    return {"success": True, "data": None, "message": "API 運作中"}
