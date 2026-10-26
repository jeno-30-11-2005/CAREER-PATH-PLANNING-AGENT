from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.models.entities import CareerRole
from backend.app.schemas.career_schemas import CareerRoleResponse
from backend.app.services.career_service import CareerService

router = APIRouter(prefix="/careers", tags=["Career Roles Knowledge Base"])

@router.get("/", response_model=List[CareerRoleResponse])
def get_career_roles(db: Session = Depends(get_db)):
    return CareerService.get_all(db)

@router.get("/{slug}", response_model=CareerRoleResponse)
def get_career_role(slug: str, db: Session = Depends(get_db)):
    role = CareerService.get_by_slug(db, slug)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career role '{slug}' not found in knowledge base."
        )
    return role
