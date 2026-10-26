from fastapi import APIRouter
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "llm_provider": "Google Gemini" if settings.GEMINI_API_KEY else "Deterministic Offline Engine"
    }
