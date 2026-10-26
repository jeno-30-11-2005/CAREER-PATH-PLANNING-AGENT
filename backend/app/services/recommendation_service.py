from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from backend.app.models.entities import StudentProfile, CareerRole, CareerRecommendation
from backend.app.schemas.career_schemas import RecommendationItem, CareerRoleResponse

class RecommendationEngine:
    # Configurable weights for transparent, deterministic scoring
    WEIGHT_SKILLS = 0.40
    WEIGHT_INTERESTS = 0.30
    WEIGHT_FIELD_PREFERENCE = 0.15
    WEIGHT_EXPERIENCE = 0.10
    WEIGHT_GOALS = 0.05

    @classmethod
    def normalize_str(cls, text: str) -> str:
        return text.strip().lower()

    @classmethod
    def calculate_skill_match(cls, student_skills: List[str], role_required: List[str], role_recommended: List[str]) -> Tuple[float, List[str], List[str]]:
        if not role_required:
            return 0.0, [], []
        
        normalized_student = {cls.normalize_str(s) for s in student_skills}
        matching_skills = []
        missing_skills = []

        # Check required skills (higher priority)
        required_matches = 0
        for req in role_required:
            req_norm = cls.normalize_str(req)
            # direct or substring matching
            matched = any(req_norm in s or s in req_norm for s in normalized_student)
            if matched:
                required_matches += 1
                matching_skills.append(req)
            else:
                missing_skills.append(req)

        # Check recommended skills
        rec_matches = 0
        for rec in role_recommended:
            rec_norm = cls.normalize_str(rec)
            matched = any(rec_norm in s or s in rec_norm for s in normalized_student)
            if matched:
                rec_matches += 1
                if rec not in matching_skills:
                    matching_skills.append(rec)

        # Score formulation: Required skills weighted 75%, recommended weighted 25%
        req_ratio = required_matches / len(role_required) if role_required else 0
        rec_ratio = rec_matches / len(role_recommended) if role_recommended else 0
        combined_skill_score = (0.75 * req_ratio) + (0.25 * rec_ratio)

        return min(combined_skill_score, 1.0), matching_skills, missing_skills

    @classmethod
    def calculate_interest_match(cls, student_interests: List[str], role: CareerRole) -> Tuple[float, List[str]]:
        if not student_interests:
            return 0.0, []

        role_corpus = f"{role.title} {role.category} {role.description} {' '.join(role.tools_technologies)}".lower()
        matched_interests = []

        for interest in student_interests:
            norm_interest = cls.normalize_str(interest)
            if norm_interest in role_corpus:
                matched_interests.append(interest)

        match_ratio = len(matched_interests) / len(student_interests) if student_interests else 0.0
        return min(match_ratio, 1.0), matched_interests

    @classmethod
    def calculate_field_preference_match(cls, preferred_fields: List[str], role: CareerRole) -> float:
        if not preferred_fields:
            return 0.5 # Neutral baseline if omitted

        role_text = f"{role.category} {role.title}".lower()
        for field in preferred_fields:
            if cls.normalize_str(field) in role_text or role_text in cls.normalize_str(field):
                return 1.0
        return 0.2

    @classmethod
    def calculate_experience_compatibility(cls, experience_level: str, role: CareerRole) -> float:
        exp = cls.normalize_str(experience_level)
        # All roles in our student curriculum have beginner onboarding paths
        if exp == "advanced":
            return 1.0
        elif exp == "intermediate":
            return 0.9
        elif exp == "beginner":
            return 0.8
        return 0.7

    @classmethod
    def calculate_goals_match(cls, career_goals: str, role: CareerRole) -> float:
        if not career_goals:
            return 0.5
        norm_goals = cls.normalize_str(career_goals)
        role_tokens = [cls.normalize_str(t) for t in [role.title, role.category] + role.tools_technologies[:3]]
        matches = sum(1 for t in role_tokens if t in norm_goals)
        return min(0.5 + (matches * 0.2), 1.0)

    @classmethod
    def evaluate_profile(cls, student: StudentProfile, roles: List[CareerRole]) -> List[RecommendationItem]:
        recommendations = []

        for role in roles:
            # 1. Skill Match
            skill_score, matching_skills, missing_skills = cls.calculate_skill_match(
                student.technical_skills or [],
                role.required_skills or [],
                role.recommended_skills or []
            )

            # 2. Interest Match
            interest_score, matching_interests = cls.calculate_interest_match(
                student.interests or [],
                role
            )

            # 3. Preferred Field Match
            field_score = cls.calculate_field_preference_match(
                student.preferred_career_fields or [],
                role
            )

            # 4. Experience Match
            exp_score = cls.calculate_experience_compatibility(
                student.programming_experience or "Beginner",
                role
            )

            # 5. Career Goals Match
            goal_score = cls.calculate_goals_match(
                student.career_goals or "",
                role
            )

            # Compute weighted composite score (0 to 100 scale)
            composite_score = (
                (cls.WEIGHT_SKILLS * skill_score) +
                (cls.WEIGHT_INTERESTS * interest_score) +
                (cls.WEIGHT_FIELD_PREFERENCE * field_score) +
                (cls.WEIGHT_EXPERIENCE * exp_score) +
                (cls.WEIGHT_GOALS * goal_score)
            ) * 100.0

            normalized_score = round(max(15.0, min(composite_score, 98.5)), 1)

            # Generate explainable justification
            explanation_parts = []
            if matching_skills:
                explanation_parts.append(
                    f"You already demonstrate baseline familiarity with {len(matching_skills)} relevant skills ({', '.join(matching_skills[:3])})."
                )
            if matching_interests:
                explanation_parts.append(
                    f"Your passion for {', '.join(matching_interests[:2])} aligns closely with the daily responsibilities of a {role.title}."
                )
            if not matching_skills and not matching_interests:
                explanation_parts.append(
                    f"This role aligns with foundational computer science trajectories in {role.category}."
                )
            
            explanation = " ".join(explanation_parts)

            # Suggested next steps
            next_steps = []
            if missing_skills:
                next_steps.append(f"Prioritize building foundations in: {missing_skills[0]}")
                if len(missing_skills) > 1:
                    next_steps.append(f"Explore hands-on practice with {missing_skills[1]}")
            if role.example_projects:
                next_steps.append(f"Build a capstone portfolio project: '{role.example_projects[0]}'")

            role_response = CareerRoleResponse.model_validate(role)
            item = RecommendationItem(
                career_role=role_response,
                match_score=normalized_score,
                matching_interests=matching_interests,
                matching_skills=matching_skills,
                missing_skills=missing_skills,
                explanation=explanation,
                suggested_next_steps=next_steps
            )
            recommendations.append(item)

        # Sort descending by match score
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations
