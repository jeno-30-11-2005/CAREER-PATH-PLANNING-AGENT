# test_system.py
# Purpose: Automated verification script for Intelligent Career Path Planning System.
# Tests recommendation scoring, skill-gap analysis, and roadmap retrieval.

import sys
from career_data import CAREER_DATABASE, AVAILABLE_SKILLS, AVAILABLE_INTERESTS
from logic import calculate_career_matches, analyze_skill_gap

def run_tests():
    print("=" * 60)
    print("RUNNING AUTOMATED TESTS: Career Path Planning System")
    print("=" * 60)

    # Test Case 1: Knowledge Base Integrity
    print("\n[Test 1] Verifying Career Database Structure...")
    assert len(CAREER_DATABASE) == 4, "Must contain exactly 4 careers"
    expected_careers = ["AI Engineer", "ML Engineer", "Data Analyst", "Python Developer"]
    for c in expected_careers:
        assert c in CAREER_DATABASE, f"Missing career: {c}"
        assert len(CAREER_DATABASE[c]["required_skills"]) > 0, f"Skills empty for {c}"
        assert len(CAREER_DATABASE[c]["roadmap"]) == 4, f"Roadmap must have 4 steps for {c}"
    print("  -> Passed: All 4 careers and roadmaps verified.")

    # Test Case 2: Recommendation Scoring for AI-Focused Student
    print("\n[Test 2] Testing Career Recommendation for AI-Focused Student...")
    student_skills = ["Python", "Prompt Engineering", "FastAPI"]
    student_interests = ["Artificial Intelligence", "Generative AI"]
    
    recs = calculate_career_matches(student_skills, student_interests)
    assert len(recs) == 4, "Should evaluate all 4 careers"
    top_match = recs[0]
    assert top_match["career_name"] == "AI Engineer", f"Expected AI Engineer as top match, got {top_match['career_name']}"
    assert top_match["match_score"] > 0, "Match score must be positive"
    print(f"  -> Passed: Top career is '{top_match['title']}' with score {top_match['match_score']}%.")

    # Test Case 3: Skill-Gap Analysis
    print("\n[Test 3] Testing Skill-Gap Analysis for ML Engineer...")
    student_skills = ["Python", "NumPy & Pandas"]
    gap = analyze_skill_gap(student_skills, "ML Engineer")
    
    assert "Python" in gap["acquired"], "Python should be in acquired skills"
    assert "NumPy & Pandas" in gap["acquired"], "NumPy & Pandas should be in acquired skills"
    assert "Scikit-Learn" in gap["missing"], "Scikit-Learn should be in missing skills"
    assert len(gap["acquired"]) + len(gap["missing"]) == gap["total_required"]
    print(f"  -> Passed: Acquired {len(gap['acquired'])} skills, Missing {len(gap['missing'])} skills.")

    # Test Case 4: Edge Case - Empty Student Profile
    print("\n[Test 4] Testing Edge Case: Completely Empty Skills and Interests...")
    empty_recs = calculate_career_matches([], [])
    assert len(empty_recs) == 4
    for r in empty_recs:
        assert r["match_score"] == 0.0 or r["match_score"] >= 0
    print("  -> Passed: System handles empty inputs gracefully without exceptions.")

    # Test Case 5: Roadmap Completeness
    print("\n[Test 5] Testing Roadmap Step Ordering & Timeline...")
    for career_key, data in CAREER_DATABASE.items():
        roadmap = data["roadmap"]
        steps = [item["step"] for item in roadmap]
        assert "Step 1: Foundations" in steps[0] or "Step 1:" in steps[0]
        assert "Step 4:" in steps[3]
    print("  -> Passed: All roadmaps contain proper progressive steps.")

    print("\n" + "=" * 60)
    print("ALL 5 TESTS PASSED SUCCESSFULLY! (100% Verified)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
