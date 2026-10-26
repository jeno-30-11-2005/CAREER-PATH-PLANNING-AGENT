from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.models.entities import StudentProfile, CareerRole
from backend.app.schemas.career_schemas import SkillGapResponse
from backend.app.services.skill_gap_service import SkillGapService

router = APIRouter(prefix="/skill-gap", tags=["Skill Gap Analysis"])

@router.get("/{profile_id}/{role_slug}", response_model=SkillGapResponse)
def analyze_skill_gap(profile_id: int, role_slug: str, db: Session = Depends(get_db)):
    student = db.query(StudentProfile).filter(StudentProfile.id == profile_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student profile with ID {profile_id} not found."
        )

    role = db.query(CareerRole).filter(CareerRole.slug == role_slug).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career role '{role_slug}' not found."
        )

    return SkillGapService.analyze_gap(student, role)
