from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
import datetime

# --- Student Profile Schemas ---
class StudentProfileBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, description="Full or display name")
    education_level: str = Field(..., description="e.g. Undergraduate, Postgraduate")
    degree_specialization: str = Field(..., description="e.g. BE AI & Data Science")
    current_year_sem: str = Field(..., description="e.g. 3rd Year, Semester 6")
    interests: List[str] = Field(default_factory=list, description="List of technical/domain interests")
    technical_skills: List[str] = Field(default_factory=list, description="Reported technical skills")
    soft_skills: List[str] = Field(default_factory=list, description="Reported soft skills")
    programming_experience: str = Field(..., description="Beginner, Intermediate, or Advanced")
    preferred_career_fields: List[str] = Field(default_factory=list, description="Preferred industry/tech fields")
    weekly_learning_hours: int = Field(default=10, ge=1, le=80, description="Available study hours per week")
    career_goals: Optional[str] = Field(None, max_length=1000, description="Personal aspirations or notes")

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileUpdate(BaseModel):
    name: Optional[str] = None
    education_level: Optional[str] = None
    degree_specialization: Optional[str] = None
    current_year_sem: Optional[str] = None
    interests: Optional[List[str]] = None
    technical_skills: Optional[List[str]] = None
    soft_skills: Optional[List[str]] = None
    programming_experience: Optional[str] = None
    preferred_career_fields: Optional[List[str]] = None
    weekly_learning_hours: Optional[int] = Field(None, ge=1, le=80)
    career_goals: Optional[str] = None

class StudentProfileResponse(StudentProfileBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)


# --- Career Role Schemas ---
class CareerRoleBase(BaseModel):
    slug: str
    title: str
    category: str
    description: str
    required_skills: List[str]
    recommended_skills: List[str]
    tools_technologies: List[str]
    example_projects: List[str]
    learning_sequence: List[str]
    prerequisites: List[str]

class CareerRoleResponse(CareerRoleBase):
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)


# --- Recommendation Schemas ---
class RecommendationItem(BaseModel):
    career_role: CareerRoleResponse
    match_score: float = Field(..., ge=0.0, le=100.0)
    matching_interests: List[str]
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str
    suggested_next_steps: List[str]

class RecommendationResponse(BaseModel):
    student_id: int
    recommendations: List[RecommendationItem]
    scoring_methodology: str
    timestamp: datetime.datetime


# --- Skill Gap Schemas ---
class SkillGapItem(BaseModel):
    skill: str
    category: str # "core" or "recommended"
    status: str # "confirmed", "partial", "unreported"
    priority: int # 1 = highest priority
    prerequisites: List[str] = Field(default_factory=list)

class SkillGapResponse(BaseModel):
    career_role_title: str
    career_role_slug: str
    total_required_skills: int
    confirmed_skills: List[str]
    partially_developed_skills: List[str]
    not_yet_reported_skills: List[str]
    detailed_skills: List[SkillGapItem]
    recommended_learning_order: List[str]
    disclaimer: str


# --- Roadmap Schemas ---
class RoadmapItemBase(BaseModel):
    phase: str
    step_number: int
    skill_topic: str
    why_it_matters: str
    prerequisites: List[str] = Field(default_factory=list)
    suggested_activity: str
    estimated_effort_hours: int
    practical_exercise: str
    milestone_project: str
    completion_status: str = "not_started"
    resource_links: List[Dict[str, str]] = Field(default_factory=list)
    learning_notes: Optional[str] = None

class RoadmapItemResponse(RoadmapItemBase):
    id: int
    roadmap_id: int
    model_config = ConfigDict(from_attributes=True)

class RoadmapItemUpdate(BaseModel):
    completion_status: Optional[str] = Field(None, pattern="^(not_started|in_progress|completed)$")
    learning_notes: Optional[str] = None

class LearningRoadmapResponse(BaseModel):
    id: int
    student_profile_id: int
    career_role_id: int
    title: str
    target_role: str
    weekly_hours: int
    total_estimated_weeks: int
    is_approved: bool
    generation_method: str
    items: List[RoadmapItemResponse]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class RoadmapApprovalRequest(BaseModel):
    is_approved: bool = True
    edited_items: Optional[List[Dict[str, Any]]] = None


# --- AI Chat Schemas ---
class ChatMessageCreate(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[int] = None
    career_role_slug: Optional[str] = None
    student_profile_id: Optional[int] = None

class ChatMessageResponse(BaseModel):
    session_id: int
    role: str
    content: str
    is_fallback: bool
    timestamp: datetime.datetime
    sources: List[str] = Field(default_factory=list)


# --- Dashboard Overview Schema ---
class DashboardOverviewResponse(BaseModel):
    student_profile: Optional[StudentProfileResponse]
    profile_completeness_percentage: int
    recommended_roles_count: int
    active_roadmap: Optional[LearningRoadmapResponse]
    completed_steps_count: int
    total_steps_count: int
    overall_progress_percentage: float
    next_skills_to_learn: List[str]
