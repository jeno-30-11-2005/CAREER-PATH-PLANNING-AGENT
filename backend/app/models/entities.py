import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    education_level = Column(String(80), nullable=False) # e.g. "Undergraduate", "Postgraduate"
    degree_specialization = Column(String(120), nullable=False) # e.g. "BE AI & Data Science"
    current_year_sem = Column(String(50), nullable=False) # e.g. "3rd Year, Semester 6"
    interests = Column(JSON, default=list) # e.g. ["Machine Learning", "Cloud Systems"]
    technical_skills = Column(JSON, default=list) # e.g. ["Python", "SQL", "Pandas"]
    soft_skills = Column(JSON, default=list) # e.g. ["Critical Thinking", "Communication"]
    programming_experience = Column(String(50), nullable=False) # "Beginner", "Intermediate", "Advanced"
    preferred_career_fields = Column(JSON, default=list) # e.g. ["Artificial Intelligence", "Data Engineering"]
    weekly_learning_hours = Column(Integer, default=10)
    career_goals = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    recommendations = relationship("CareerRecommendation", back_populates="student", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="student", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="student", cascade="all, delete-orphan")


class CareerRole(Base):
    __tablename__ = "career_roles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(80), unique=True, index=True, nullable=False) # e.g. "ml-engineer"
    title = Column(String(120), nullable=False) # e.g. "Machine Learning Engineer"
    category = Column(String(80), nullable=False) # e.g. "AI & Data Science"
    description = Column(Text, nullable=False)
    required_skills = Column(JSON, default=list) # Primary non-negotiable skills
    recommended_skills = Column(JSON, default=list) # Beneficial additional skills
    tools_technologies = Column(JSON, default=list) # Frameworks, libraries, tools
    example_projects = Column(JSON, default=list) # Concrete portfolio project ideas
    learning_sequence = Column(JSON, default=list) # Suggested step phases
    prerequisites = Column(JSON, default=list) # Baseline knowledge required
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CareerRecommendation(Base):
    __tablename__ = "career_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    career_role_id = Column(Integer, ForeignKey("career_roles.id"), nullable=False)
    match_score = Column(Float, nullable=False) # e.g. 84.5
    matching_interests = Column(JSON, default=list)
    matching_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    explanation = Column(Text, nullable=False)
    suggested_next_steps = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    student = relationship("StudentProfile", back_populates="recommendations")
    career_role = relationship("CareerRole")


class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    career_role_id = Column(Integer, ForeignKey("career_roles.id"), nullable=False)
    title = Column(String(200), nullable=False)
    target_role = Column(String(120), nullable=False)
    weekly_hours = Column(Integer, default=10)
    total_estimated_weeks = Column(Integer, default=12)
    is_approved = Column(Boolean, default=False) # Human-in-the-loop review status
    generation_method = Column(String(50), default="deterministic") # "deterministic" or "agent_enhanced"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    student = relationship("StudentProfile", back_populates="roadmaps")
    career_role = relationship("CareerRole")
    items = relationship("RoadmapItem", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapItem.step_number")


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("learning_roadmaps.id"), nullable=False)
    phase = Column(String(80), nullable=False) # "1. Foundations", "2. Core Skills", "3. Applied Practice", "4. Portfolio Projects", "5. Interview Prep"
    step_number = Column(Integer, nullable=False)
    skill_topic = Column(String(120), nullable=False)
    why_it_matters = Column(Text, nullable=False)
    prerequisites = Column(JSON, default=list)
    suggested_activity = Column(Text, nullable=False)
    estimated_effort_hours = Column(Integer, default=10)
    practical_exercise = Column(Text, nullable=False)
    milestone_project = Column(Text, nullable=False)
    completion_status = Column(String(30), default="not_started") # "not_started", "in_progress", "completed"
    resource_links = Column(JSON, default=list)
    learning_notes = Column(Text, nullable=True)

    # Relationships
    roadmap = relationship("LearningRoadmap", back_populates="items")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=True)
    title = Column(String(150), default="Career Guidance Session")
    selected_role_slug = Column(String(80), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    student = relationship("StudentProfile", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.timestamp")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False) # "user", "assistant", "system"
    content = Column(Text, nullable=False)
    is_fallback = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    session = relationship("ChatSession", back_populates="messages")
