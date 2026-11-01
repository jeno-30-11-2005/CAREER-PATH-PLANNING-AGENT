# tests/test_recommendations.py
"""
Automated Unit and Integration Tests for Recommendation and Skill Gap Engines.
"""
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.connection import get_db_session
from services.recommendation_service import RecommendationEngine
from services.skill_gap_service import SkillGapService

def run_recommendation_tests():
    print("==================================================")
    print("RUNNING RECOMMENDATION & SKILL GAP ENGINE TESTS")
    print("==================================================")

    with get_db_session() as session:
        # Test 1: Generate recommendations for AI / Python profile
        profile_ai = {
            "skills": {
                "Python": "Advanced",
                "FastAPI": "Intermediate",
                "PyTorch Framework": "Intermediate",
                "Docker Containerization": "Beginner"
            },
            "interests": ["Artificial Intelligence", "Deep Learning Architectures"],
            "academic_branch": "CSE",
            "education_level": "Bachelor's in CS",
            "weekly_learning_hours": 15
        }

        recs = RecommendationEngine.get_recommendations(session, profile_ai, top_k=5)
        assert len(recs) == 5, f"Expected 5 recommendations, got {len(recs)}"
        top_rec = recs[0]
        assert top_rec["compatibility_score"] > 0, "Compatibility score should be > 0"
        assert len(top_rec["matched_essential_skills"]) > 0, "Should have matched essential skills"
        print(f"[PASS] Generated top recommendations successfully!")
        print(f"       Top match: '{top_rec['title']}' ({top_rec['category_name']}) - {top_rec['compatibility_score']}%")
        print(f"       Explanation: {top_rec['explanation']}")

        # Test 2: Skill Gap Analysis on Top Career
        gap = SkillGapService.analyze_gap(session, top_rec["career_id"], profile_ai)
        assert "readiness_percentage" in gap, "Gap analysis missing readiness_percentage"
        assert "estimated_weeks_needed" in gap, "Gap analysis missing estimated_weeks_needed"
        assert len(gap["actionable_advice"]) > 0, "Should generate actionable advice"
        print(f"[PASS] Skill Gap Analysis computed successfully!")
        print(f"       Target: {gap['title']}")
        print(f"       Readiness: {gap['readiness_percentage']}%")
        print(f"       Acquired: {gap['acquired_count']} | Missing: {gap['missing_count']} | Upgrades Needed: {gap['upgrades_needed_count']}")
        print(f"       Estimated Time: {gap['estimated_weeks_needed']} weeks ({gap['estimated_hours_needed']} hours @ {gap['weekly_study_hours']} hrs/wk)")
        for advice in gap["actionable_advice"]:
            print(f"       * {advice}")

        # Test 3: Recommendation for Web Dev / Frontend Profile
        profile_web = {
            "skills": {
                "JavaScript (ES6+)": "Advanced",
                "React.js Component Architecture": "Intermediate",
                "HTML5 & Semantic Markup": "Advanced",
                "Tailwind CSS": "Intermediate"
            },
            "interests": ["Full Stack Web Development", "Human-Computer Interaction"],
            "academic_branch": "IT",
            "education_level": "B.Tech in IT",
            "weekly_learning_hours": 20
        }
        web_recs = RecommendationEngine.get_recommendations(session, profile_web, top_k=3)
        assert len(web_recs) == 3
        print(f"[PASS] Web developer profile test passed!")
        print(f"       Top match: '{web_recs[0]['title']}' - {web_recs[0]['compatibility_score']}%")

        print("==================================================")
        print("ALL RECOMMENDATION & SKILL GAP TESTS PASSED (100%)")
        print("==================================================")

if __name__ == "__main__":
    run_recommendation_tests()
