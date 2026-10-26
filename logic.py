# logic.py
# Purpose: Contains simple, explainable mathematical logic for:
# 1. Recommending careers based on skill and interest matching.
# 2. Calculating the skill gap between a student's skills and a target career.

from career_data import CAREER_DATABASE

def calculate_career_matches(student_skills, student_interests):
    """
    Compares student's reported skills and interests with each career.
    Formula:
      Match Score = (Skill Match Ratio * 70%) + (Interest Match Ratio * 30%)
    Weights explainability: Skills are weighted 70% because technical requirements
    are essential for engineering roles; interests are weighted 30%.
    """
    results = []

    # Clean student inputs (case-insensitive matching)
    cleaned_skills = {s.strip().lower() for s in student_skills}
    cleaned_interests = {i.strip().lower() for i in student_interests}

    for career_key, career_info in CAREER_DATABASE.items():
        required_skills = career_info["required_skills"]
        related_interests = career_info["related_interests"]

        # 1. Check matching and missing skills
        matching_skills = []
        missing_skills = []
        for req in required_skills:
            if req.strip().lower() in cleaned_skills:
                matching_skills.append(req)
            else:
                missing_skills.append(req)

        # 2. Check matching interests
        matching_interests = []
        for interest in related_interests:
            if interest.strip().lower() in cleaned_interests:
                matching_interests.append(interest)

        # 3. Compute simple ratios
        skill_ratio = len(matching_skills) / len(required_skills) if required_skills else 0.0
        interest_ratio = len(matching_interests) / len(related_interests) if related_interests else 0.0

        # 4. Calculate total score on a 0 to 100 percentage scale
        total_score = round(((skill_ratio * 0.70) + (interest_ratio * 0.30)) * 100, 1)

        # Minimum baseline of 20% if at least one interest matches
        if total_score == 0 and len(matching_interests) > 0:
            total_score = 25.0

        results.append({
            "career_name": career_key,
            "title": career_info["title"],
            "description": career_info["description"],
            "match_score": total_score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "matching_interests": matching_interests,
            "total_required": len(required_skills)
        })

    # Sort careers from highest match score to lowest
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results


def analyze_skill_gap(student_skills, career_name):
    """
    Returns skills the student already possesses and skills they still need to learn.
    """
    career = CAREER_DATABASE.get(career_name)
    if not career:
        return {"acquired": [], "missing": []}

    cleaned_skills = {s.strip().lower() for s in student_skills}
    acquired = []
    missing = []

    for skill in career["required_skills"]:
        if skill.strip().lower() in cleaned_skills:
            acquired.append(skill)
        else:
            missing.append(skill)

    return {
        "acquired": acquired,
        "missing": missing,
        "total_required": len(career["required_skills"]),
        "completion_percentage": round((len(acquired) / len(career["required_skills"])) * 100, 1)
    }
