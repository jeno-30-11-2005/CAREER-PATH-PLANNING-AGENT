from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.models.entities import StudentProfile
from backend.app.schemas.career_schemas import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse
)

router = APIRouter(prefix="/profiles", tags=["Student Profiles"])

@router.post("/", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile_in: StudentProfileCreate, db: Session = Depends(get_db)):
    db_profile = StudentProfile(**profile_in.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/", response_model=List[StudentProfileResponse])
def list_profiles(db: Session = Depends(get_db)):
    return db.query(StudentProfile).order_by(StudentProfile.id.desc()).all()

@router.get("/{profile_id}", response_model=StudentProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student profile with ID {profile_id} not found."
        )
    return profile

@router.put("/{profile_id}", response_model=StudentProfileResponse)
def update_profile(profile_id: int, profile_update: StudentProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student profile with ID {profile_id} not found."
        )
    
    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile
