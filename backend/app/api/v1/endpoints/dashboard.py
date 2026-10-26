from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.db.session import get_db
from backend.app.models.entities import StudentProfile, CareerRole, LearningRoadmap, CareerRecommendation
from backend.app.schemas.career_schemas import DashboardOverviewResponse, StudentProfileResponse, LearningRoadmapResponse

router = APIRouter(prefix="/dashboard", tags=["Student Dashboard"])

@router.get("/{profile_id}", response_model=DashboardOverviewResponse)
def get_dashboard_data(profile_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentProfile).filter(StudentProfile.id == profile_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student profile with ID {profile_id} not found."
        )

    # 1. Profile completeness calculation
    completeness = 100
    if not student.technical_skills:
        completeness -= 30
    if not student.interests:
        completeness -= 25
    if not student.career_goals:
        completeness -= 15
    completeness = max(30, completeness)

    # 2. Recommendations count
    recs_count = db.query(CareerRecommendation).filter(
        CareerRecommendation.student_profile_id == profile_id
    ).count()

    # 3. Active approved roadmap
    active_roadmap = db.query(LearningRoadmap).filter(
        LearningRoadmap.student_profile_id == profile_id,
        LearningRoadmap.is_approved == True
    ).order_by(LearningRoadmap.id.desc()).first()

    completed_steps = 0
    total_steps = 0
    progress_percentage = 0.0
    next_skills = []

    if active_roadmap and active_roadmap.items:
        total_steps = len(active_roadmap.items)
        completed_steps = sum(1 for item in active_roadmap.items if item.completion_status == "completed")
        progress_percentage = round((completed_steps / total_steps) * 100.0, 1) if total_steps > 0 else 0.0

        for item in active_roadmap.items:
            if item.completion_status in ["not_started", "in_progress"]:
                next_skills.append(item.skill_topic)
                if len(next_skills) >= 3:
                    break

    return DashboardOverviewResponse(
        student_profile=StudentProfileResponse.model_validate(student),
        profile_completeness_percentage=completeness,
        recommended_roles_count=recs_count,
        active_roadmap=LearningRoadmapResponse.model_validate(active_roadmap) if active_roadmap else None,
        completed_steps_count=completed_steps,
        total_steps_count=total_steps,
        overall_progress_percentage=progress_percentage,
        next_skills_to_learn=next_skills
    )
