import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.models.entities import StudentProfile, CareerRole, CareerRecommendation
from backend.app.schemas.career_schemas import RecommendationResponse, RecommendationItem
from backend.app.services.recommendation_service import RecommendationEngine

router = APIRouter(prefix="/recommendations", tags=["Career Recommendations"])

@router.post("/generate/{profile_id}", response_model=RecommendationResponse)
def generate_recommendations(profile_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentProfile).filter(StudentProfile.id == profile_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student profile with ID {profile_id} not found."
        )

    roles = db.query(CareerRole).all()
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Career knowledge base is empty. Initialize seed data first."
        )

    ranked_items = RecommendationEngine.evaluate_profile(student, roles)
    top_3 = ranked_items[:3]

    # Save to history
    for item in top_3:
        rec = CareerRecommendation(
            student_profile_id=student.id,
            career_role_id=item.career_role.id,
            match_score=item.match_score,
            matching_interests=item.matching_interests,
            matching_skills=item.matching_skills,
            missing_skills=item.missing_skills,
            explanation=item.explanation,
            suggested_next_steps=item.suggested_next_steps
        )
        db.add(rec)
    db.commit()

    return RecommendationResponse(
        student_id=student.id,
        recommendations=top_3,
        scoring_methodology="Deterministic Multi-Factor Weighted Scoring (40% Skills, 30% Interests, 15% Field, 10% Experience, 5% Goals)",
        timestamp=datetime.datetime.utcnow()
    )
