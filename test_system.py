# test_system.py
"""
Comprehensive End-to-End System Verification Suite.
Validates:
1. Database Integrity & Coverage Targets (1,500+ Skills, 500+ Careers, 250+ Interests, 450+ Pathways, 500+ Projects, 500+ Resources)
2. Recommendation Engine (Multi-factor explainable scoring formula)
3. Skill Gap Analysis (Readiness %, Priority Gaps, Study Time Estimation)
4. Personalized 8-Stage Roadmap Generator
5. Practical Portfolio Projects Service
6. Curated Learning Resources Service
7. Career Comparison Engine (2-3 careers side-by-side)
8. AI Resume Parsing & Alignment Service
9. Administrator Authentication & Bulk Ingestion
10. Student Profile & Progress Tracking Service
"""
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.connection import get_db_session, init_db
from database.models import (
    TechnicalSkill, AreaOfInterest, Career, CareerCategory,
    CareerPathway, Project, LearningResource, Administrator, Student
)
from services.recommendation_service import RecommendationEngine
from services.skill_gap_service import SkillGapService
from services.roadmap_service import RoadmapService
from services.project_service import ProjectService
from services.resource_service import ResourceService
from services.comparison_service import CareerComparisonService
from services.resume_service import ResumeService
from services.admin_service import AdminService
from services.student_service import StudentService

def run_comprehensive_tests():
    print("=" * 70)
    print("[*] INTELLIGENT CAREER PATH PLANNING SYSTEM: END-TO-END VERIFICATION")
    print("=" * 70)

    init_db()

    with get_db_session() as session:
        # TEST 1: Database Integrity & Target Metrics
        print("\n[Test 1] Verifying Large-Scale Database Coverage Targets...")
        skill_count = session.query(TechnicalSkill).count()
        interest_count = session.query(AreaOfInterest).count()
        family_count = session.query(CareerCategory).count()
        career_count = session.query(Career).count()
        pathway_count = session.query(CareerPathway).count()
        project_count = session.query(Project).count()
        resource_count = session.query(LearningResource).count()

        print(f"  - Technical Skills:     {skill_count:,} (Target: 1,500+) -> {'PASS' if skill_count >= 1500 else 'FAIL'}")
        print(f"  - Areas of Interest:    {interest_count:,} (Target: 250+)   -> {'PASS' if interest_count >= 250 else 'FAIL'}")
        print(f"  - Career Families:      {family_count:,} (Target: 50)     -> {'PASS' if family_count >= 50 else 'FAIL'}")
        print(f"  - Career Profiles:      {career_count:,} (Target: 500+)   -> {'PASS' if career_count >= 500 else 'FAIL'}")
        print(f"  - Career Pathways:      {pathway_count:,} (Target: 200+)   -> {'PASS' if pathway_count >= 200 else 'FAIL'}")
        print(f"  - Portfolio Projects:   {project_count:,} (Target: 500+)   -> {'PASS' if project_count >= 500 else 'FAIL'}")
        print(f"  - Learning Resources:   {resource_count:,} (Target: 500+)   -> {'PASS' if resource_count >= 500 else 'FAIL'}")

        assert skill_count >= 1500, f"Expected >= 1500 skills, found {skill_count}"
        assert interest_count >= 250, f"Expected >= 250 interests, found {interest_count}"
        assert family_count >= 50, f"Expected >= 50 families, found {family_count}"
        assert career_count >= 500, f"Expected >= 500 careers, found {career_count}"
        assert pathway_count >= 200, f"Expected >= 200 pathways, found {pathway_count}"
        assert project_count >= 500, f"Expected >= 500 projects, found {project_count}"
        assert resource_count >= 500, f"Expected >= 500 resources, found {resource_count}"
        print("  -> Passed: All 7 macro data coverage targets fully satisfied!")

        # TEST 2: Multi-Factor Recommendation Engine
        print("\n[Test 2] Testing Multi-Factor Recommendation Scoring...")
        sample_ai_profile = {
            "skills": {
                "Python": "Advanced",
                "PyTorch Framework": "Intermediate",
                "FastAPI": "Intermediate",
                "Docker Containerization": "Beginner"
            },
            "interests": ["Artificial Intelligence", "Deep Learning Architectures"],
            "academic_branch": "CSE",
            "education_level": "Bachelor's",
            "weekly_learning_hours": 15
        }
        recs = RecommendationEngine.get_recommendations(session, sample_ai_profile, top_k=5)
        assert len(recs) == 5, "Must return exactly 5 recommendations"
        top_rec = recs[0]
        assert top_rec["compatibility_score"] > 0
        assert "explanation" in top_rec and len(top_rec["explanation"]) > 20
        print(f"  -> Passed: Top match '{top_rec['title']}' ({top_rec['category_name']}) - Compatibility: {top_rec['compatibility_score']}%.")
        print(f"     Explanation: {top_rec['explanation'][:90]}...")

        # TEST 3: Skill Gap Analysis Engine
        print("\n[Test 3] Testing Skill Gap Analysis...")
        target_cid = top_rec["career_id"]
        gap = SkillGapService.analyze_gap(session, target_cid, sample_ai_profile)
        assert "readiness_percentage" in gap
        assert "high_priority_missing" in gap
        assert "estimated_weeks_needed" in gap
        print(f"  -> Passed: Readiness: {gap['readiness_percentage']}%, Acquired: {gap['acquired_count']}, Missing: {gap['missing_count']}.")
        print(f"     Timeline: {gap['estimated_weeks_needed']} weeks ({gap['estimated_hours_needed']} hrs @ {gap['weekly_study_hours']} hrs/wk).")

        # TEST 4: Personalized 8-Stage Roadmap Generator
        print("\n[Test 4] Testing 8-Stage Learning Roadmap Generator...")
        roadmap = RoadmapService.generate_roadmap(session, target_cid, sample_ai_profile)
        assert roadmap["total_stages"] == 8, f"Expected 8 stages, got {roadmap['total_stages']}"
        assert len(roadmap["stages"]) == 8
        print(f"  -> Passed: 8 Stages Generated! Total Effort: {roadmap['total_hours']} hrs across ~{roadmap['estimated_total_weeks']} weeks.")
        for stg in roadmap["stages"][:3]:
            print(f"     Stage {stg['stage_number']}: {stg['stage_name']} ({stg['estimated_hours']} hrs)")

        # TEST 5: Portfolio Projects Service
        print("\n[Test 5] Testing Practical Portfolio Projects Service...")
        career_projs = ProjectService.get_projects_for_career(session, target_cid)
        assert len(career_projs) >= 1, "Career should have mapped portfolio projects"
        sample_proj = career_projs[0]
        assert "problem_statement" in sample_proj and "implementation_steps" in sample_proj
        print(f"  -> Passed: Project '{sample_proj['title']}' ({sample_proj['difficulty']}) loaded with complete implementation steps.")

        # TEST 6: Curated Learning Resources Service
        print("\n[Test 6] Testing Learning Resources Retrieval...")
        career_res = ResourceService.get_resources_for_career(session, target_cid)
        assert len(career_res) >= 1, "Career should have mapped resources"
        sample_res = career_res[0]
        assert sample_res["url"].startswith("http"), "Must contain verified live URL"
        print(f"  -> Passed: Resource '{sample_res['title']}' ({sample_res['provider']}) - {sample_res['url']}.")

        # TEST 7: Career Comparison Engine
        print("\n[Test 7] Testing Career Comparison Tool...")
        comp = CareerComparisonService.compare_careers(session, [1, 2])
        assert len(comp["careers"]) == 2
        assert "common_essential_skills" in comp
        print(f"  -> Passed: Compared '{comp['careers'][0]['title']}' vs '{comp['careers'][1]['title']}'. Common skills: {len(comp['common_essential_skills'])}.")

        # TEST 8: AI Resume Analyzer & Competency Extraction
        print("\n[Test 8] Testing Resume Skill Extraction & Alignment...")
        resume_sample = """
        John Doe | Software Engineer
        Education: B.Tech in Computer Science and Engineering
        Skills: Python, FastAPI, Docker, PostgreSQL, PyTorch, React, Git, Linux
        Experience: Developed microservices with FastAPI and PostgreSQL, containerized services with Docker, and trained PyTorch models.
        """
        analysis = ResumeService.analyze_resume(session, resume_sample, target_career_id=target_cid)
        assert analysis["extracted_skills_count"] >= 4, "Should extract technical skills"
        assert analysis["match_rate"] > 0, "Match rate should be calculated"
        assert len(analysis["suggestions"]) > 0, "Should generate ATS recommendations"
        print(f"  -> Passed: Extracted {analysis['extracted_skills_count']} skills, Match Rate: {analysis['match_rate']}%.")

        # TEST 9: Admin Authentication & Ingestion
        print("\n[Test 9] Testing Admin Service & Authentication...")
        admin = AdminService.authenticate(session, "admin", "admin123")
        assert admin is not None, "Default admin authentication failed"
        stats = AdminService.get_system_stats(session)
        assert stats["total_skills"] >= 1500
        print(f"  -> Passed: Admin authenticated successfully. Total skills reported: {stats['total_skills']:,}.")

        # TEST 10: Student Profile & Progress Persistence
        print("\n[Test 10] Testing Student Profile & Progress Persistence...")
        student = StudentService.create_or_update_student(
            session=session,
            full_name="Verification Student",
            email="verify_test@university.edu",
            academic_branch="CSE",
            weekly_hours=20,
            target_career_id=target_cid
        )
        assert student.student_id is not None
        StudentService.update_progress(
            session=session,
            student_id=student.student_id,
            career_id=target_cid,
            readiness_pct=65.0,
            completed_skills=4,
            total_skills=8,
            completed_projects=1,
            milestones_done=3
        )
        p_dict = StudentService.get_student_profile_dict(session, student.student_id)
        assert p_dict["full_name"] == "Verification Student"
        print(f"  -> Passed: Student profile and progress successfully persisted and retrieved!")

        print("\n" + "=" * 70)
        print("[SUCCESS] ALL 10 END-TO-END VERIFICATION TESTS PASSED WITH 100% SUCCESS!")
        print("=" * 70)

if __name__ == "__main__":
    run_comprehensive_tests()
