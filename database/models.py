# database/models.py
"""
Normalized Relational Database Models for Intelligent Career Path Planning System.
Defines 25 interconnected tables for skills, interests, careers, pathways,
recommendations, learning resources, projects, roadmaps, and student tracking.
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime,
    ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# ============================================================================
# 1. TECHNICAL SKILLS SUBSYSTEM
# ============================================================================

class SkillCategory(Base):
    """Categorization for skills (e.g. Programming Languages, AI, Cloud, DevOps)."""
    __tablename__ = "skill_categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    domain = Column(String(100), nullable=False, index=True) # Broad cluster (e.g. Software, Data, Infrastructure, Hardware)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    skills = relationship("TechnicalSkill", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SkillCategory(id={self.category_id}, name='{self.name}')>"


class TechnicalSkill(Base):
    """Individual technical skill (target: 1,500+ records)."""
    __tablename__ = "technical_skills"

    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_code = Column(String(100), unique=True, nullable=False, index=True) # Normalized slug
    name = Column(String(150), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("skill_categories.category_id", ondelete="CASCADE"), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=False)
    difficulty_level = Column(String(30), default="Intermediate", index=True) # Beginner, Intermediate, Advanced, Expert
    learning_priority = Column(String(20), default="High") # High, Medium, Low
    industry_relevance = Column(String(30), default="High") # Critical, High, Moderate, Emerging
    is_active = Column(Boolean, default=True, index=True)
    verification_status = Column(String(30), default="Verified") # Verified, Curated, Estimated, User-generated
    source = Column(String(150), default="Curated Engineering Taxonomy")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("SkillCategory", back_populates="skills")
    aliases = relationship("SkillAlias", back_populates="skill", cascade="all, delete-orphan")
    career_associations = relationship("CareerSkill", back_populates="skill", cascade="all, delete-orphan")
    project_associations = relationship("ProjectSkill", back_populates="skill", cascade="all, delete-orphan")
    learning_resources = relationship("LearningResource", back_populates="skill", cascade="all, delete-orphan")
    student_skills = relationship("StudentSkill", back_populates="skill", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TechnicalSkill(id={self.skill_id}, name='{self.name}')>"


class SkillAlias(Base):
    """Alternative spellings, acronyms, and aliases for search matching (e.g. JS -> JavaScript)."""
    __tablename__ = "skill_aliases"

    alias_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("technical_skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)
    alias_name = Column(String(150), nullable=False, index=True)

    # Relationships
    skill = relationship("TechnicalSkill", back_populates="aliases")

    __table_args__ = (
        UniqueConstraint("skill_id", "alias_name", name="uq_skill_alias"),
    )


class SkillRelationship(Base):
    """Prerequisites, complementary skills, and advanced progressions between skills."""
    __tablename__ = "skill_relationships"

    rel_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("technical_skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)
    related_skill_id = Column(Integer, ForeignKey("technical_skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_type = Column(String(50), nullable=False) # prerequisite, complementary, advanced_progression

    __table_args__ = (
        UniqueConstraint("skill_id", "related_skill_id", "relationship_type", name="uq_skill_relationship"),
    )


# ============================================================================
# 2. AREAS OF INTEREST SUBSYSTEM
# ============================================================================

class InterestCategory(Base):
    """Broad domain categories for student interests."""
    __tablename__ = "interest_categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    interests = relationship("AreaOfInterest", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InterestCategory(id={self.category_id}, name='{self.name}')>"


class AreaOfInterest(Base):
    """Specific interest areas (target: 250+ records)."""
    __tablename__ = "areas_of_interest"

    interest_id = Column(Integer, primary_key=True, autoincrement=True)
    interest_code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("interest_categories.category_id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    industry_domain = Column(String(100), nullable=True, index=True)
    learning_difficulty = Column(String(30), default="Intermediate")

    # Relationships
    category = relationship("InterestCategory", back_populates="interests")
    career_associations = relationship("CareerInterest", back_populates="interest", cascade="all, delete-orphan")
    student_interests = relationship("StudentInterest", back_populates="interest", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AreaOfInterest(id={self.interest_id}, name='{self.name}')>"


class InterestRelationship(Base):
    """Interconnections between related interest areas."""
    __tablename__ = "interest_relationships"

    rel_id = Column(Integer, primary_key=True, autoincrement=True)
    interest_id = Column(Integer, ForeignKey("areas_of_interest.interest_id", ondelete="CASCADE"), nullable=False, index=True)
    related_interest_id = Column(Integer, ForeignKey("areas_of_interest.interest_id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("interest_id", "related_interest_id", name="uq_interest_rel"),
    )


# ============================================================================
# 3. CAREERS & PROGRESSION SUBSYSTEM
# ============================================================================

class CareerCategory(Base):
    """Career families (e.g. AI & ML, Data Science, Cloud, Cybersecurity, Embedded)."""
    __tablename__ = "career_categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False, index=True) # A, B, C...
    name = Column(String(150), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    careers = relationship("Career", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CareerCategory(id={self.category_id}, name='{self.name}')>"


class Career(Base):
    """Comprehensive career profile (target: 500+ records)."""
    __tablename__ = "careers"

    career_id = Column(Integer, primary_key=True, autoincrement=True)
    career_code = Column(String(100), unique=True, nullable=False, index=True) # slug
    title = Column(String(150), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("career_categories.category_id", ondelete="CASCADE"), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=False)
    daily_responsibilities = Column(Text, nullable=False)
    required_education = Column(String(150), default="Bachelor's in Engineering/CS/Data Science or equivalent")
    preferred_education = Column(String(150), default="B.E. / B.Tech / M.Tech / M.S.")
    relevant_branches = Column(Text, nullable=False) # e.g. "CSE, AI & DS, IT, ECE"
    soft_skills = Column(Text, nullable=True) # Comma-separated or bullet points
    recommended_certifications = Column(Text, nullable=True) # Verified or marked curated
    difficulty_level = Column(String(30), default="Intermediate") # Beginner, Intermediate, Advanced
    entry_level_suitability = Column(String(30), default="Moderate", index=True) # High (fresher friendly), Moderate, Low, Experienced
    career_progression = Column(Text, nullable=True) # Junior -> Mid -> Senior trajectory
    junior_roles = Column(Text, nullable=True)
    mid_roles = Column(Text, nullable=True)
    senior_roles = Column(Text, nullable=True)
    industry_sectors = Column(Text, nullable=True) # e.g. "Tech, Healthcare, Finance, E-commerce"
    verification_status = Column(String(30), default="Curated") # Verified, Curated, Estimated
    source = Column(String(150), default="ACM/IEEE & Industry Standards")
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("CareerCategory", back_populates="careers")
    skills = relationship("CareerSkill", back_populates="career", cascade="all, delete-orphan")
    interests = relationship("CareerInterest", back_populates="career", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="career", cascade="all, delete-orphan")
    learning_resources = relationship("LearningResource", back_populates="career", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="career", cascade="all, delete-orphan")
    outgoing_pathways = relationship("CareerPathway", foreign_keys="CareerPathway.starting_career_id", back_populates="starting_career", cascade="all, delete-orphan")
    incoming_pathways = relationship("CareerPathway", foreign_keys="CareerPathway.next_career_id", back_populates="next_career", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Career(id={self.career_id}, title='{self.title}')>"


class CareerSkill(Base):
    """Maps essential, preferred, and additional skills to a career with proficiency requirements."""
    __tablename__ = "career_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("technical_skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)
    skill_type = Column(String(20), default="essential", index=True) # essential (70%), preferred (20%), additional (10%)
    required_proficiency = Column(String(20), default="Intermediate") # Beginner, Intermediate, Advanced, Expert
    importance_weight = Column(Float, default=1.0)

    # Relationships
    career = relationship("Career", back_populates="skills")
    skill = relationship("TechnicalSkill", back_populates="career_associations")

    __table_args__ = (
        UniqueConstraint("career_id", "skill_id", name="uq_career_skill"),
    )


class CareerInterest(Base):
    """Maps career relevance to areas of interest."""
    __tablename__ = "career_interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="CASCADE"), nullable=False, index=True)
    interest_id = Column(Integer, ForeignKey("areas_of_interest.interest_id", ondelete="CASCADE"), nullable=False, index=True)
    relevance_weight = Column(Float, default=1.0)

    # Relationships
    career = relationship("Career", back_populates="interests")
    interest = relationship("AreaOfInterest", back_populates="career_associations")

    __table_args__ = (
        UniqueConstraint("career_id", "interest_id", name="uq_career_interest"),
    )


class CareerPathway(Base):
    """Career transition pathways and progression routes (target: 200+ pathways)."""
    __tablename__ = "career_pathways"

    pathway_id = Column(Integer, primary_key=True, autoincrement=True)
    starting_career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="CASCADE"), nullable=False, index=True)
    next_career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="CASCADE"), nullable=False, index=True)
    progression_type = Column(String(50), default="Vertical Progression") # Vertical Progression, Lateral Specialization, Cross-Domain
    required_skills_delta = Column(Text, nullable=False) # Skills needed to make the jump
    additional_learning = Column(Text, nullable=True)
    recommended_projects = Column(Text, nullable=True)
    estimated_duration_months = Column(Integer, default=6)
    preparation_guidelines = Column(Text, nullable=True)
    verification_status = Column(String(30), default="Curated")

    # Relationships
    starting_career = relationship("Career", foreign_keys=[starting_career_id], back_populates="outgoing_pathways")
    next_career = relationship("Career", foreign_keys=[next_career_id], back_populates="incoming_pathways")

    __table_args__ = (
        UniqueConstraint("starting_career_id", "next_career_id", "progression_type", name="uq_career_pathway"),
    )


# ============================================================================
# 4. LEARNING RESOURCES & PROJECTS SUBSYSTEM
# ============================================================================

class LearningResource(Base):
    """Curated learning materials, docs, and courses (target: 500+ records)."""
    __tablename__ = "learning_resources"

    resource_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    provider = Column(String(100), nullable=False, index=True) # e.g. Python Docs, Mozilla MDN, Harvard CS50, Coursera, FreeCodeCamp
    url = Column(String(300), nullable=False)
    skill_id = Column(Integer, ForeignKey("technical_skills.skill_id", ondelete="SET NULL"), nullable=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="SET NULL"), nullable=True, index=True)
    resource_type = Column(String(50), default="Official Documentation", index=True) # Official Documentation, Free Course, Video Tutorial, Practice Platform, Technical Book
    difficulty = Column(String(30), default="Beginner") # Beginner, Intermediate, Advanced
    is_free = Column(Boolean, default=True, index=True)
    language = Column(String(30), default="English")
    last_verified = Column(String(30), default=datetime.utcnow().strftime("%Y-%m-%d"))
    verification_status = Column(String(30), default="Verified") # Verified, Curated, Community
    is_active = Column(Boolean, default=True)

    # Relationships
    skill = relationship("TechnicalSkill", back_populates="learning_resources")
    career = relationship("Career", back_populates="learning_resources")

    def __repr__(self):
        return f"<LearningResource(id={self.resource_id}, title='{self.title}')>"


class Project(Base):
    """Practical real-world projects organized by career and skills (target: 500+ records)."""
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="SET NULL"), nullable=True, index=True)
    category = Column(String(100), nullable=False, index=True) # e.g. "Machine Learning", "Full Stack Web"
    difficulty = Column(String(30), default="Intermediate", index=True) # Beginner, Intermediate, Advanced
    estimated_hours = Column(Integer, default=20)
    project_type = Column(String(30), default="Individual") # Individual, Team / Capstone
    problem_statement = Column(Text, nullable=False)
    objective = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    suggested_technologies = Column(Text, nullable=False) # e.g. "Python, Scikit-Learn, Streamlit"
    implementation_steps = Column(Text, nullable=False) # Bulleted or numbered roadmap
    expected_deliverables = Column(Text, nullable=False)
    learning_outcomes = Column(Text, nullable=False)
    suggested_extensions = Column(Text, nullable=True)

    # Relationships
    career = relationship("Career", back_populates="projects")
    skill_associations = relationship("ProjectSkill", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.project_id}, title='{self.title}')>"


class ProjectSkill(Base):
    """Maps required skills to specific projects."""
    __tablename__ = "project_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("technical_skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    project = relationship("Project", back_populates="skill_associations")
    skill = relationship("TechnicalSkill", back_populates="project_associations")

    __table_args__ = (
        UniqueConstraint("project_id", "skill_id", name="uq_project_skill"),
    )


# ============================================================================
# 5. STUDENT PROFILES & PROGRESS TRACKING SUBSYSTEM
# ============================================================================

class Student(Base):
    """Student academic profile and career aspirations."""
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(120), nullable=False, index=True)
    email = Column(String(120), nullable=True, index=True)
    education_level = Column(String(80), default="Undergraduate") # Undergraduate, Postgraduate, Diploma
    degree = Column(String(120), default="BE / B.Tech") # B.Tech / B.E., B.Sc, BCA, etc.
    academic_branch = Column(String(120), default="Artificial Intelligence & Data Science") # AI & DS, CSE, IT, ECE
    current_year = Column(String(50), default="3rd Year") # 1st Year, 2nd Year, 3rd Year, 4th Year
    semester = Column(String(30), default="Semester 6")
    graduation_year = Column(Integer, default=datetime.utcnow().year + 1)
    weekly_learning_hours = Column(Integer, default=10)
    preferred_learning_method = Column(String(80), default="Hands-on Projects") # Hands-on Projects, Video Tutorials, Documentation
    preferred_career_family = Column(String(120), nullable=True)
    target_career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="SET NULL"), nullable=True)
    career_aspiration = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    interests = relationship("StudentInterest", back_populates="student", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="student", cascade="all, delete-orphan")
    progress_records = relationship("StudentProgress", back_populates="student", cascade="all, delete-orphan")
    recommendation_logs = relationship("RecommendationHistory", back_populates="student", cascade="all, delete-orphan")
    resume_analyses = relationship("ResumeAnalysis", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(id={self.student_id}, name='{self.full_name}')>"


class StudentSkill(Base):
    """Skills possessed by a student with self-reported or assessed proficiency."""
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("technical_skills.skill_id", ondelete="CASCADE"), nullable=True, index=True)
    proficiency_level = Column(String(20), default="Intermediate") # Beginner, Intermediate, Advanced, Expert
    is_custom = Column(Boolean, default=False)
    custom_skill_name = Column(String(150), nullable=True)
    date_added = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="skills")
    skill = relationship("TechnicalSkill", back_populates="student_skills")


class StudentInterest(Base):
    """Areas of interest selected by a student."""
    __tablename__ = "student_interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    interest_id = Column(Integer, ForeignKey("areas_of_interest.interest_id", ondelete="CASCADE"), nullable=True, index=True)
    is_custom = Column(Boolean, default=False)
    custom_interest_name = Column(String(150), nullable=True)

    # Relationships
    student = relationship("Student", back_populates="interests")
    interest = relationship("AreaOfInterest", back_populates="student_interests")


class StudentProgress(Base):
    """Tracks milestone completion and readiness for a target career."""
    __tablename__ = "student_progress"

    progress_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="CASCADE"), nullable=False, index=True)
    completed_skills_count = Column(Integer, default=0)
    total_required_skills = Column(Integer, default=0)
    completed_projects_count = Column(Integer, default=0)
    milestones_completed = Column(Text, default="[]") # JSON list of milestone titles
    overall_readiness_pct = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="progress_records")
    career = relationship("Career")


# ============================================================================
# 6. ROADMAPS & RECOMMENDATIONS SUBSYSTEM
# ============================================================================

class LearningRoadmap(Base):
    """Personalized 8-stage learning roadmap tailored to student weekly hours."""
    __tablename__ = "learning_roadmaps"

    roadmap_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    total_stages = Column(Integer, default=8)
    weekly_hours = Column(Integer, default=10)
    estimated_total_weeks = Column(Integer, default=16)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="roadmaps")
    career = relationship("Career", back_populates="roadmaps")
    items = relationship("RoadmapItem", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapItem.stage_number")


class RoadmapItem(Base):
    """Individual milestones within an 8-stage roadmap."""
    __tablename__ = "roadmap_items"

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    roadmap_id = Column(Integer, ForeignKey("learning_roadmaps.roadmap_id", ondelete="CASCADE"), nullable=False, index=True)
    stage_number = Column(Integer, nullable=False) # 1 to 8
    stage_name = Column(String(100), nullable=False) # Foundations, Core, Advanced, Projects, Portfolio, Resume, Interview, Internships
    topic_title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    milestone = Column(Text, nullable=False)
    estimated_hours = Column(Integer, default=15)
    is_completed = Column(Boolean, default=False, index=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    roadmap = relationship("LearningRoadmap", back_populates="items")


class RecommendationHistory(Base):
    """Historical audit of generated career recommendations."""
    __tablename__ = "recommendation_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="CASCADE"), nullable=False, index=True)
    compatibility_score = Column(Float, nullable=False)
    matched_essential_skills = Column(Text, default="[]") # JSON list
    missing_essential_skills = Column(Text, default="[]") # JSON list
    matched_preferred_skills = Column(Text, default="[]") # JSON list
    missing_preferred_skills = Column(Text, default="[]") # JSON list
    explanation = Column(Text, nullable=False)
    computed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="recommendation_logs")
    career = relationship("Career")


# ============================================================================
# 7. RESUME ANALYSIS, ADMIN & DATA AUDIT SUBSYSTEM
# ============================================================================

class ResumeAnalysis(Base):
    """Stored results from parsed PDF / DOCX resumes."""
    __tablename__ = "resume_analysis"

    analysis_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="SET NULL"), nullable=True, index=True)
    file_name = Column(String(200), nullable=False)
    extracted_text = Column(Text, nullable=True)
    extracted_skills = Column(Text, default="[]") # JSON list of detected skills
    target_career_id = Column(Integer, ForeignKey("careers.career_id", ondelete="SET NULL"), nullable=True)
    matched_skills = Column(Text, default="[]")
    missing_skills = Column(Text, default="[]")
    improvement_suggestions = Column(Text, nullable=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="resume_analyses")
    target_career = relationship("Career")


class Administrator(Base):
    """Authorized administrators for CRUD operations and data imports."""
    __tablename__ = "administrators"

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="ContentManager") # SuperAdmin, ContentManager, Auditor
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DataImportLog(Base):
    """Audit trail for batch CSV and JSON imports."""
    __tablename__ = "data_import_logs"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_type = Column(String(50), nullable=False) # skills, interests, careers, projects, resources
    source_format = Column(String(20), nullable=False) # CSV, JSON
    total_records = Column(Integer, default=0)
    inserted_records = Column(Integer, default=0)
    rejected_records = Column(Integer, default=0)
    error_log = Column(Text, nullable=True)
    imported_by = Column(String(80), default="System")
    timestamp = Column(DateTime, default=datetime.utcnow)
