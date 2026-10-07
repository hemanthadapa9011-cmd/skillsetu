from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router

app = FastAPI(title="SkillSetu 2.0", version="0.1.0")

app.include_router(auth_router)
app.include_router(admin_router)


@app.get("/")
def read_root():
    return {"app": "SkillSetu 2.0", "status": "running"}
