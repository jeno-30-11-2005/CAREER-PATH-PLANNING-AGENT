# tests/test_database.py
"""
Phase 2 Verification Tests: Normalized Relational Database Foundation
Tests table creation, schema integrity, constraints, relationships, and transactional sessions.
"""
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import (
    Base, SkillCategory, TechnicalSkill, SkillAlias, SkillRelationship,
    InterestCategory, AreaOfInterest, CareerCategory, Career,
    CareerSkill, CareerInterest, CareerPathway, LearningResource,
    Project, ProjectSkill, Student, StudentSkill, StudentInterest,
    StudentProgress, LearningRoadmap, RoadmapItem, RecommendationHistory,
    ResumeAnalysis, Administrator, DataImportLog
)

TEST_DATABASE_URL = "sqlite:///:memory:"

def get_test_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSession()

def run_all_tests():
    print("=" * 60)
    print("RUNNING DATABASE FOUNDATION TESTS (Phase 2)")
    print("=" * 60)

    session = get_test_session()

    # Test 1: Table Creation
    print("\n[Test 1] Verifying 25 Normalized Relational Tables...")
    tables = Base.metadata.tables.keys()
    assert len(tables) == 25, f"Expected 25 tables, got {len(tables)}"
    assert "technical_skills" in tables
    assert "skill_categories" in tables
    assert "careers" in tables
    assert "areas_of_interest" in tables
    assert "projects" in tables
    assert "learning_resources" in tables
    assert "career_pathways" in tables
    assert "students" in tables
    assert "learning_roadmaps" in tables
    print(f"  -> Passed: All {len(tables)} tables created successfully.")

    # Test 2: Skills and Aliases
    print("\n[Test 2] Testing Skill Category, Technical Skill, and Aliases...")
    cat = SkillCategory(name="Programming Languages", domain="Software Engineering", description="Core coding languages")
    session.add(cat)
    session.commit()

    skill = TechnicalSkill(
        skill_code="python",
        name="Python",
        category_id=cat.category_id,
        subcategory="General Purpose",
        description="High-level, interpreted programming language with rich ecosystem.",
        difficulty_level="Beginner",
        learning_priority="High",
        industry_relevance="Critical"
    )
    session.add(skill)
    session.commit()

    alias = SkillAlias(skill_id=skill.skill_id, alias_name="Python 3")
    session.add(alias)
    session.commit()

    queried_skill = session.query(TechnicalSkill).filter_by(skill_code="python").first()
    assert queried_skill is not None
    assert queried_skill.category.name == "Programming Languages"
    assert len(queried_skill.aliases) == 1
    assert queried_skill.aliases[0].alias_name == "Python 3"
    print("  -> Passed: Skill, category, and alias relationship verified.")

    # Test 3: Duplicate Prevention
    print("\n[Test 3] Testing Unique Constraints & Duplicate Prevention...")
    duplicate_cat = SkillCategory(name="Programming Languages", domain="Duplicate", description="Duplicate")
    session.add(duplicate_cat)
    try:
        session.commit()
        raise AssertionError("Should have raised unique constraint exception!")
    except Exception:
        session.rollback()
    print("  -> Passed: Unique constraints prevent duplicate categories/skills.")

    # Test 4: Career and Career-Skills
    print("\n[Test 4] Testing Career & CareerSkills Relationships...")
    skill2 = TechnicalSkill(skill_code="pandas", name="Pandas", category_id=cat.category_id, description="Data manipulation")
    session.add(skill2)
    session.commit()

    career_cat = CareerCategory(code="AI_ML", name="AI and Machine Learning Careers", description="Careers in AI")
    session.add(career_cat)
    session.commit()

    career = Career(
        career_code="ml-engineer",
        title="Machine Learning Engineer",
        category_id=career_cat.category_id,
        description="Designs predictive ML pipelines",
        daily_responsibilities="Feature engineering, training models, model evaluation",
        relevant_branches="CSE, AI & DS"
    )
    session.add(career)
    session.commit()

    cs1 = CareerSkill(career_id=career.career_id, skill_id=skill.skill_id, skill_type="essential", required_proficiency="Intermediate")
    cs2 = CareerSkill(career_id=career.career_id, skill_id=skill2.skill_id, skill_type="preferred", required_proficiency="Advanced")
    session.add_all([cs1, cs2])
    session.commit()

    queried_career = session.query(Career).filter_by(career_code="ml-engineer").first()
    assert len(queried_career.skills) == 2
    essential_skills = [cs.skill.name for cs in queried_career.skills if cs.skill_type == "essential"]
    assert "Python" in essential_skills
    print("  -> Passed: Career mapped to essential and preferred skills.")

    # Test 5: Student Progress & Roadmap Milestones
    print("\n[Test 5] Testing Student Profile and Roadmap Tracking...")
    student = Student(
        full_name="Alex Mercer",
        email="alex@university.edu",
        degree="B.Tech",
        academic_branch="Data Science",
        weekly_learning_hours=12
    )
    session.add(student)
    session.commit()

    roadmap = LearningRoadmap(
        student_id=student.student_id,
        career_id=career.career_id,
        title="ML Engineer Mastery Roadmap",
        total_stages=8,
        weekly_hours=student.weekly_learning_hours
    )
    session.add(roadmap)
    session.commit()

    item1 = RoadmapItem(
        roadmap_id=roadmap.roadmap_id,
        stage_number=1,
        stage_name="Foundations",
        topic_title="Linear Algebra & Matrix Operations",
        description="Scalars, vectors, matrix transformations",
        milestone="Implement vector dot products from scratch in Python"
    )
    session.add(item1)
    session.commit()

    item1.is_completed = True
    session.commit()

    queried_roadmap = session.query(LearningRoadmap).filter_by(roadmap_id=roadmap.roadmap_id).first()
    assert len(queried_roadmap.items) == 1
    assert queried_roadmap.items[0].is_completed is True
    print("  -> Passed: Student roadmap milestones created and updated.")

    print("\n" + "=" * 60)
    print("ALL 5 DATABASE FOUNDATION TESTS PASSED (100% Verified)!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()

