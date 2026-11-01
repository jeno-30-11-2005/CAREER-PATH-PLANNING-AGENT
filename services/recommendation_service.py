# services/recommendation_service.py
"""
Multi-Factor Career Recommendation Engine.
Implements an explainable, weighted compatibility scoring algorithm:
- 70% Essential Skills matching
- 20% Preferred Skills matching
- 10% Additional Skills matching
- Academic branch & education qualification alignment
- Areas of interest affinity boost
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from database.models import (
    Career, CareerCategory, CareerSkill, CareerInterest,
    TechnicalSkill, AreaOfInterest, Student, StudentSkill, StudentInterest,
    RecommendationHistory
)

PROFICIENCY_WEIGHTS = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3,
    "expert": 4
}

def compute_proficiency_factor(student_level: str, required_level: str) -> float:
    """
    Computes a fractional score (0.0 to 1.0) based on student's proficiency vs. required.
    If student meets or exceeds requirement: 1.0.
    If student is below requirement, awards partial credit.
    """
    s_val = PROFICIENCY_WEIGHTS.get(str(student_level).lower().strip(), 1)
    r_val = PROFICIENCY_WEIGHTS.get(str(required_level).lower().strip(), 2)

    if s_val >= r_val:
        return 1.0
    elif s_val == r_val - 1:
        return 0.75
    elif s_val == r_val - 2:
        return 0.50
    else:
        return 0.30

class RecommendationEngine:
    @staticmethod
    def get_recommendations(
        session: Session,
        student_profile: Dict[str, Any],
        top_k: int = 10,
        category_id: Optional[int] = None,
        difficulty_filter: Optional[str] = None,
        save_history: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Calculates compatibility scores for careers against the student profile.
        
        student_profile can contain:
          - student_id: Optional[int]
          - skills: Dict[int, str] or Dict[str, str] (skill_id or name -> proficiency)
          - interests: List[int] or List[str] (interest_ids or names)
          - academic_branch: str (e.g. 'CSE', 'ECE', 'IT', 'Mechanical')
          - education_level: str (e.g. "Bachelor's", "Master's")
          - weekly_learning_hours: int
        """
        # 1. Normalize student skills map
        student_skills_raw = student_profile.get("skills", {})
        student_skills: Dict[int, str] = {} # skill_id -> proficiency

        # Pre-cache technical skills
        all_skills = session.query(TechnicalSkill).all()
        skill_name_to_id = {s.name.lower(): s.skill_id for s in all_skills}
        skill_id_to_skill = {s.skill_id: s for s in all_skills}

        if isinstance(student_skills_raw, dict):
            for k, prof in student_skills_raw.items():
                if isinstance(k, int):
                    student_skills[k] = prof
                elif isinstance(k, str):
                    if k.isdigit():
                        student_skills[int(k)] = prof
                    elif k.lower() in skill_name_to_id:
                        student_skills[skill_name_to_id[k.lower()]] = prof
        elif isinstance(student_skills_raw, list):
            for item in student_skills_raw:
                if isinstance(item, dict):
                    s_id = item.get("skill_id")
                    prof = item.get("proficiency", "Intermediate")
                    if s_id and s_id in skill_id_to_skill:
                        student_skills[s_id] = prof

        # 2. Normalize student interests
        student_interests_raw = student_profile.get("interests", [])
        student_interest_ids = set()
        all_interests = session.query(AreaOfInterest).all()
        interest_name_to_id = {i.name.lower(): i.interest_id for i in all_interests}

        for item in student_interests_raw:
            if isinstance(item, int):
                student_interest_ids.add(item)
            elif isinstance(item, str):
                if item.isdigit():
                    student_interest_ids.add(int(item))
                elif item.lower() in interest_name_to_id:
                    student_interest_ids.add(interest_name_to_id[item.lower()])

        student_branch = str(student_profile.get("academic_branch", "")).lower().strip()
        student_edu = str(student_profile.get("education_level", "")).lower().strip()

        # 3. Query candidate careers
        query = session.query(Career).join(CareerCategory)
        if category_id:
            query = query.filter(Career.category_id == category_id)
        if difficulty_filter:
            query = query.filter(Career.difficulty_level.ilike(f"%{difficulty_filter}%"))

        candidate_careers = query.all()
        recommendations = []

        for career in candidate_careers:
            # Partition career skills
            essential_skills = []
            preferred_skills = []
            additional_skills = []

            for cs in career.skills:
                sk_obj = skill_id_to_skill.get(cs.skill_id)
                if not sk_obj:
                    continue
                info = {
                    "skill_id": cs.skill_id,
                    "name": sk_obj.name,
                    "category": sk_obj.category.name if sk_obj.category else "Technology",
                    "required_proficiency": cs.required_proficiency,
                    "importance_weight": cs.importance_weight
                }
                if cs.skill_type == "essential":
                    essential_skills.append(info)
                elif cs.skill_type == "preferred":
                    preferred_skills.append(info)
                else:
                    additional_skills.append(info)

            # A. Essential Skills Score (70% weight)
            ess_matched = []
            ess_missing = []
            ess_score_sum = 0.0

            for es in essential_skills:
                s_id = es["skill_id"]
                req_prof = es["required_proficiency"]
                if s_id in student_skills:
                    stu_prof = student_skills[s_id]
                    factor = compute_proficiency_factor(stu_prof, req_prof)
                    ess_score_sum += factor
                    ess_matched.append({
                        **es,
                        "student_proficiency": stu_prof,
                        "proficiency_factor": factor,
                        "status": "Acquired" if factor == 1.0 else "Needs Advance"
                    })
                else:
                    ess_missing.append(es)

            ess_pct = (ess_score_sum / len(essential_skills)) if essential_skills else 1.0

            # B. Preferred Skills Score (20% weight)
            pref_matched = []
            pref_missing = []
            pref_score_sum = 0.0

            for ps in preferred_skills:
                s_id = ps["skill_id"]
                req_prof = ps["required_proficiency"]
                if s_id in student_skills:
                    stu_prof = student_skills[s_id]
                    factor = compute_proficiency_factor(stu_prof, req_prof)
                    pref_score_sum += factor
                    pref_matched.append({
                        **ps,
                        "student_proficiency": stu_prof,
                        "proficiency_factor": factor,
                        "status": "Acquired" if factor == 1.0 else "Needs Advance"
                    })
                else:
                    pref_missing.append(ps)

            pref_pct = (pref_score_sum / len(preferred_skills)) if preferred_skills else 1.0

            # C. Additional Skills Score (10% weight)
            add_matched = []
            add_missing = []
            add_score_sum = 0.0

            for ads in additional_skills:
                s_id = ads["skill_id"]
                req_prof = ads["required_proficiency"]
                if s_id in student_skills:
                    stu_prof = student_skills[s_id]
                    factor = compute_proficiency_factor(stu_prof, req_prof)
                    add_score_sum += factor
                    add_matched.append({
                        **ads,
                        "student_proficiency": stu_prof,
                        "proficiency_factor": factor,
                        "status": "Acquired"
                    })
                else:
                    add_missing.append(ads)

            add_pct = (add_score_sum / len(additional_skills)) if additional_skills else 1.0

            # Weighted base skill score (0 to 100)
            raw_skill_score = (0.70 * ess_pct) + (0.20 * pref_pct) + (0.10 * add_pct)
            skill_score = round(raw_skill_score * 100, 1)

            # D. Interest Alignment
            career_interest_ids = {ci.interest_id for ci in career.interests}
            matched_interest_ids = student_interest_ids.intersection(career_interest_ids)
            matched_interests_list = [
                i.name for i in all_interests if i.interest_id in matched_interest_ids
            ]

            interest_score = 0.0
            if career_interest_ids:
                interest_score = (len(matched_interest_ids) / len(career_interest_ids)) * 100
            elif student_interest_ids:
                # If career has no explicit interest tags, check text match with career family
                cat_name_low = career.category.name.lower()
                for intr_name in [i.name.lower() for i in all_interests if i.interest_id in student_interest_ids]:
                    if intr_name in cat_name_low or cat_name_low in intr_name:
                        interest_score = 75.0
                        break

            # E. Academic Alignment
            edu_score = 50.0 # Neutral baseline
            career_branches_low = (career.relevant_branches or "").lower()
            if student_branch:
                # Direct match
                if any(b.strip() in career_branches_low for b in student_branch.split(",")):
                    edu_score = 100.0
                elif any(common in career_branches_low and common in student_branch for common in ["cs", "it", "ee", "ec", "mech", "data"]):
                    edu_score = 80.0
                else:
                    edu_score = 40.0

            # Composite Final Compatibility Score
            # If student has skills: 65% Skills, 20% Interests, 15% Academic Background
            # If beginner with no skills: 75% Interests, 25% Academic Background
            if student_skills:
                final_compatibility = (
                    (0.65 * skill_score) +
                    (0.20 * interest_score) +
                    (0.15 * edu_score)
                )
            else:
                final_compatibility = (
                    (0.75 * interest_score) +
                    (0.25 * edu_score)
                )
            final_compatibility = min(100.0, max(0.0, round(final_compatibility, 1)))

            # Generate natural language explanation
            explanation = RecommendationEngine._generate_explanation(
                career=career,
                final_score=final_compatibility,
                skill_score=skill_score,
                ess_matched=ess_matched,
                ess_missing=ess_missing,
                matched_interests=matched_interests_list,
                branch_aligned=(edu_score >= 80.0)
            )

            rec = {
                "career_id": career.career_id,
                "career_code": career.career_code,
                "title": career.title,
                "category_id": career.category_id,
                "category_name": career.category.name,
                "subcategory": career.subcategory,
                "description": career.description,
                "daily_responsibilities": career.daily_responsibilities,
                "difficulty_level": career.difficulty_level,
                "entry_level_suitability": career.entry_level_suitability,
                "required_education": career.required_education,
                "preferred_education": career.preferred_education,
                "relevant_branches": career.relevant_branches,
                "soft_skills": career.soft_skills,
                "recommended_certifications": career.recommended_certifications,
                "career_progression": career.career_progression,
                "industry_sectors": career.industry_sectors,
                "compatibility_score": final_compatibility,
                "skill_score": skill_score,
                "interest_score": round(interest_score, 1),
                "education_score": round(edu_score, 1),
                "essential_matched_count": len(ess_matched),
                "essential_total_count": len(essential_skills),
                "matched_essential_skills": ess_matched,
                "missing_essential_skills": ess_missing,
                "matched_preferred_skills": pref_matched,
                "missing_preferred_skills": pref_missing,
                "matched_additional_skills": add_matched,
                "missing_additional_skills": add_missing,
                "matched_interests": matched_interests_list,
                "explanation": explanation
            }
            recommendations.append(rec)

        # Sort descending by compatibility score
        recommendations.sort(key=lambda x: x["compatibility_score"], reverse=True)
        top_recs = recommendations[:top_k]

        # Optional persistence
        student_id = student_profile.get("student_id")
        if save_history and student_id:
            for item in top_recs[:5]:
                hist = RecommendationHistory(
                    student_id=student_id,
                    career_id=item["career_id"],
                    compatibility_score=item["compatibility_score"],
                    matched_essential_skills=",".join([s["name"] for s in item["matched_essential_skills"]]),
                    missing_essential_skills=",".join([s["name"] for s in item["missing_essential_skills"]]),
                    matched_preferred_skills=",".join([s["name"] for s in item["matched_preferred_skills"]]),
                    missing_preferred_skills=",".join([s["name"] for s in item["missing_preferred_skills"]]),
                    explanation=item["explanation"]
                )
                session.add(hist)
            session.commit()

        return top_recs

    @staticmethod
    def _generate_explanation(
        career: Career,
        final_score: float,
        skill_score: float,
        ess_matched: List[Dict],
        ess_missing: List[Dict],
        matched_interests: List[str],
        branch_aligned: bool
    ) -> str:
        """
        Synthesizes an explainable, beginner-friendly justification for the recommendation.
        """
        parts = []
        if final_score >= 80:
            parts.append(f"Outstanding match ({final_score}%) for your profile.")
        elif final_score >= 60:
            parts.append(f"Strong match ({final_score}%) with high potential.")
        elif final_score >= 40:
            parts.append(f"Moderate match ({final_score}%); requires targeted skill building.")
        else:
            parts.append(f"Emerging match ({final_score}%); foundational prerequisites needed.")

        if ess_matched:
            matched_names = [s["name"] for s in ess_matched[:3]]
            parts.append(f"You already possess key essential skills including {', '.join(matched_names)}.")
        
        if ess_missing:
            missing_names = [s["name"] for s in ess_missing[:2]]
            parts.append(f"Prioritize acquiring {', '.join(missing_names)} to maximize qualification.")
        
        if matched_interests:
            parts.append(f"Aligns directly with your passion in {', '.join(matched_interests[:2])}.")

        if branch_aligned:
            parts.append("Your academic background fits the preferred educational pathway.")

        return " ".join(parts)
