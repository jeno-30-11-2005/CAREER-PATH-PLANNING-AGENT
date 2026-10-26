from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.v1.api import api_router
from backend.app.db.init_db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="BE AI & Data Science Mini-Project: Intelligent Career Path Planning Agent with Deterministic Recommender, Skill Gap Analysis, Roadmap Generator, and AI Assistant.",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS] + ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Automatically initialize SQLite/PostgreSQL schema and seed knowledge base
    init_db()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR,
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
