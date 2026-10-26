import pytest
import sys
import os
sys.path.insert(0, os.path.abspath("."))

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.session import SessionLocal, Base, engine
from backend.app.models.entities import StudentProfile, CareerRole
from backend.app.services.recommendation_service import RecommendationEngine
from backend.app.services.skill_gap_service import SkillGapService
from backend.app.services.roadmap_service import RoadmapService
from backend.app.services.ai_assistant_service import AIAssistantService
from backend.app.agents.workflow import AgenticCareerWorkflow

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

# Test 1: System Health Endpoint
def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Intelligent Career Path Planning Agent" in data["service"]

# Test 2: Profile Creation and Schema Validation
def test_student_profile_creation(test_db):
    payload = {
        "name": "Nadia Rachel",
        "education_level": "Undergraduate",
        "degree_specialization": "BE Artificial Intelligence & Data Science",
        "current_year_sem": "3rd Year, Semester 6",
        "interests": ["Machine Learning", "Deep Learning", "Generative AI"],
        "technical_skills": ["Python", "SQL", "Pandas"],
        "soft_skills": ["Problem Solving", "Communication"],
        "programming_experience": "Intermediate",
        "preferred_career_fields": ["Artificial Intelligence & Data Science"],
        "weekly_learning_hours": 12,
        "career_goals": "Aiming to become an AI Engineer building agentic systems."
    }
    response = client.post("/api/v1/profiles/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Nadia Rachel"
    assert data["weekly_learning_hours"] == 12

# Test 3: Validation Error on Incomplete/Invalid Profile
def test_profile_validation_failure():
    # Missing required name and education_level
    invalid_payload = {
        "interests": ["Machine Learning"],
        "weekly_learning_hours": 999 # Exceeds allowed range (1-80)
    }
    response = client.post("/api/v1/profiles/", json=invalid_payload)
    assert response.status_code == 422 # Pydantic validation unprocessable entity

# Test 4: Knowledge Base Career Roles Existence
def test_career_roles_knowledge_base():
    response = client.get("/api/v1/careers/")
    assert response.status_code == 200
    roles = response.json()
    assert len(roles) >= 8
    slugs = [r["slug"] for r in roles]
    expected_slugs = [
        "ml-engineer", "ai-engineer", "data-analyst", "data-scientist",
        "backend-developer", "data-engineer", "mlops-engineer", "ai-product-engineer"
    ]
    for s in expected_slugs:
        assert s in slugs, f"Missing expected role: {s}"

# Test 5: Deterministic Recommendation Scoring & Ranking
def test_recommendation_scoring(test_db):
    student = test_db.query(StudentProfile).first()
    roles = test_db.query(CareerRole).all()
    assert student is not None
    assert len(roles) > 0

    recommendations = RecommendationEngine.evaluate_profile(student, roles)
    assert len(recommendations) == len(roles)
    # Check top match has high score and is sorted
    assert recommendations[0].match_score >= recommendations[1].match_score
    assert recommendations[0].match_score > 0
    assert len(recommendations[0].explanation) > 10

# Test 6: Skill Gap Categorization (Confirmed, Partial, Unreported)
def test_skill_gap_analysis(test_db):
    student = test_db.query(StudentProfile).first()
    role = test_db.query(CareerRole).filter(CareerRole.slug == "ml-engineer").first()
    assert student is not None
    assert role is not None

    gap = SkillGapService.analyze_gap(student, role)
    assert gap.career_role_slug == "ml-engineer"
    assert "Python" in gap.confirmed_skills # Student declared Python
    assert len(gap.not_yet_reported_skills) > 0
    assert "Educational Note" in gap.disclaimer

# Test 7: Roadmap Phase Generation & Feasibility
def test_roadmap_proposal_generation(test_db):
    student = test_db.query(StudentProfile).first()
    role = test_db.query(CareerRole).filter(CareerRole.slug == "ai-engineer").first()
    
    proposal = RoadmapService.generate_roadmap_proposal(student, role)
    assert "items" in proposal
    assert len(proposal["items"]) >= 5
    phases = {item["phase"] for item in proposal["items"]}
    assert "1. Foundations" in phases
    assert "2. Core Technical Skills" in phases
    assert "4. Portfolio Projects" in phases
    assert proposal["total_estimated_weeks"] > 0

# Test 8: Roadmap Persistence & Progress Item Update
def test_roadmap_approval_and_item_patch(test_db):
    student = test_db.query(StudentProfile).first()
    role = test_db.query(CareerRole).filter(CareerRole.slug == "ai-engineer").first()

    proposal = RoadmapService.generate_roadmap_proposal(student, role)
    # Approve and save
    response = client.post(
        f"/api/v1/roadmaps/approve/{student.id}/{role.slug}",
        json=proposal
    )
    assert response.status_code == 200
    saved = response.json()
    assert saved["is_approved"] is True
    assert len(saved["items"]) > 0

    first_item_id = saved["items"][0]["id"]
    # Patch item status to completed
    patch_res = client.patch(
        f"/api/v1/roadmaps/items/{first_item_id}",
        json={"completion_status": "completed", "learning_notes": "Completed initial foundation exercises."}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["completion_status"] == "completed"

# Test 9: Dashboard Metrics Calculation
def test_dashboard_metrics(test_db):
    student = test_db.query(StudentProfile).first()
    response = client.get(f"/api/v1/dashboard/{student.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["profile_completeness_percentage"] > 0
    assert data["completed_steps_count"] >= 1 # We just marked 1 item completed
    assert data["overall_progress_percentage"] > 0

# Test 10: AI Assistant Graceful Offline Fallback
def test_ai_assistant_fallback():
    # In test environment without Gemini key, assistant should fall back gracefully
    response = client.post(
        "/api/v1/assistant/chat",
        json={"message": "What projects should I build for Machine Learning Engineer?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_fallback"] is True # Confirms deterministic fallback active
    assert "Machine Learning" in data["content"] or "projects" in data["content"].lower()

# Test 11: Agentic Career Planning Workflow Execution
def test_agentic_workflow(test_db):
    student = test_db.query(StudentProfile).first()
    response = client.post(
        "/api/v1/workflow/run",
        json={"student_profile_id": student.id, "selected_role_slug": "ai-engineer"}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "awaiting_human_approval"
    assert result["requires_human_approval"] is True
    assert len(result["workflow_log"]) >= 6
    assert result["quality_review"]["passed"] is True
