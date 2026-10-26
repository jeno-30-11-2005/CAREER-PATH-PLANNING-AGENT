from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health,
    profiles,
    careers,
    recommendations,
    skill_gap,
    roadmaps,
    assistant,
    dashboard,
    workflow
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(profiles.router)
api_router.include_router(careers.router)
api_router.include_router(recommendations.router)
api_router.include_router(skill_gap.router)
api_router.include_router(roadmaps.router)
api_router.include_router(assistant.router)
api_router.include_router(dashboard.router)
api_router.include_router(workflow.router)
