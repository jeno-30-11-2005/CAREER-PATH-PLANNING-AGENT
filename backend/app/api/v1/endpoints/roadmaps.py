from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from backend.app.db.session import get_db
from backend.app.models.entities import StudentProfile, CareerRole, LearningRoadmap, RoadmapItem
from backend.app.schemas.career_schemas import (
    LearningRoadmapResponse,
    RoadmapItemResponse,
    RoadmapItemUpdate,
    RoadmapApprovalRequest
)
from backend.app.services.roadmap_service import RoadmapService

router = APIRouter(prefix="/roadmaps", tags=["Learning Roadmaps"])

@router.post("/propose/{profile_id}/{role_slug}")
def propose_roadmap(profile_id: int, role_slug: str, db: Session = Depends(get_db)):
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

    proposal = RoadmapService.generate_roadmap_proposal(student, role)
    return {
        "status": "proposal_generated",
        "message": "Roadmap proposal generated. Review and approve before saving.",
        "proposal": proposal
    }

@router.post("/approve/{profile_id}/{role_slug}", response_model=LearningRoadmapResponse)
def approve_and_save_roadmap(
    profile_id: int,
    role_slug: str,
    approval_body: Dict[str, Any],
    db: Session = Depends(get_db)
):
    student = db.query(StudentProfile).filter(StudentProfile.id == profile_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")

    role = db.query(CareerRole).filter(CareerRole.slug == role_slug).first()
    if not role:
        raise HTTPException(status_code=404, detail="Career role not found.")

    # Save
    saved_roadmap = RoadmapService.save_approved_roadmap(db, student.id, role.id, approval_body)
    return saved_roadmap

@router.get("/student/{profile_id}", response_model=Optional[LearningRoadmapResponse])
def get_student_roadmap(profile_id: int, db: Session = Depends(get_db)):
    roadmap = db.query(LearningRoadmap).filter(
        LearningRoadmap.student_profile_id == profile_id,
        LearningRoadmap.is_approved == True
    ).order_by(LearningRoadmap.id.desc()).first()
    return roadmap

@router.patch("/items/{item_id}", response_model=RoadmapItemResponse)
def update_roadmap_item(
    item_id: int,
    item_update: RoadmapItemUpdate,
    db: Session = Depends(get_db)
):
    item = db.query(RoadmapItem).filter(RoadmapItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap item not found.")

    update_dict = item_update.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(item, k, v)

    db.commit()
    db.refresh(item)
    return item
