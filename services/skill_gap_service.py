# services/skill_gap_service.py
"""
Skill Gap Analysis Engine.
Analyzes the exact delta between a student's current competencies and the
prerequisites of any target career:
- Readiness percentage
- Missing skills classified by priority (High, Medium, Low)
- Proficiency level gaps (e.g. Beginner -> Advanced)
- Estimated learning hours & timeline based on student's weekly study capacity
- Actionable step-by-step bridging milestones
"""
import math
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from database.models import (
    Career, CareerSkill, TechnicalSkill, Student, StudentSkill
)
from services.recommendation_service import PROFICIENCY_WEIGHTS, compute_proficiency_factor

# Base hours needed to acquire a skill from scratch to desired level
ESTIMATED_ACQUISITION_HOURS = {
    "beginner": 35,
    "intermediate": 70,
    "advanced": 130,
    "expert": 200
}

# Hours needed to upgrade one level
UPGRADE_HOURS = {
    ("beginner", "intermediate"): 35,
    ("beginner", "advanced"): 90,
    ("beginner", "expert"): 160,
    ("intermediate", "advanced"): 60,
    ("intermediate", "expert"): 120,
    ("advanced", "expert"): 70
}

class SkillGapService:
    @staticmethod
    def analyze_gap(
        session: Session,
        target_career_id: int,
        student_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Performs an in-depth skill gap analysis for a specific career.
        """
        career = session.query(Career).filter_by(career_id=target_career_id).first()
        if not career:
            raise ValueError(f"Career with ID {target_career_id} does not exist.")

        # Pre-cache technical skills
        all_skills = session.query(TechnicalSkill).all()
        skill_name_to_id = {s.name.lower(): s.skill_id for s in all_skills}
        skill_id_to_skill = {s.skill_id: s for s in all_skills}

        # Normalize student skills: skill_id -> proficiency
        student_skills_raw = student_profile.get("skills", {})
        student_skills: Dict[int, str] = {}

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

        weekly_hours = max(5, int(student_profile.get("weekly_learning_hours", 15)))

        acquired_essential = []
        missing_essential = []
        acquired_preferred = []
        missing_preferred = []
        acquired_additional = []
        missing_additional = []
        proficiency_upgrades = []

        total_hours_needed = 0
        essential_score_sum = 0.0

        for cs in career.skills:
            sk = skill_id_to_skill.get(cs.skill_id)
            if not sk:
                continue

            req_prof = cs.required_proficiency or "Intermediate"
            skill_info = {
                "skill_id": cs.skill_id,
                "name": sk.name,
                "category": sk.category.name if sk.category else "Technical",
                "subcategory": sk.subcategory,
                "description": sk.description,
                "difficulty_level": sk.difficulty_level,
                "required_proficiency": req_prof,
                "importance_weight": cs.importance_weight
            }

            if cs.skill_id in student_skills:
                curr_prof = student_skills[cs.skill_id]
                factor = compute_proficiency_factor(curr_prof, req_prof)
                is_sufficient = factor >= 1.0

                item = {
                    **skill_info,
                    "current_proficiency": curr_prof,
                    "status": "Proficient" if is_sufficient else "Needs Upgrade",
                    "proficiency_factor": factor
                }

                if cs.skill_type == "essential":
                    acquired_essential.append(item)
                    essential_score_sum += factor
                elif cs.skill_type == "preferred":
                    acquired_preferred.append(item)
                else:
                    acquired_additional.append(item)

                if not is_sufficient:
                    curr_low = str(curr_prof).lower().strip()
                    req_low = str(req_prof).lower().strip()
                    needed_hrs = UPGRADE_HOURS.get((curr_low, req_low), 40)
                    total_hours_needed += needed_hrs
                    proficiency_upgrades.append({
                        **item,
                        "current_level": curr_prof,
                        "target_level": req_prof,
                        "estimated_hours": needed_hrs
                    })
            else:
                req_low = str(req_prof).lower().strip()
                needed_hrs = ESTIMATED_ACQUISITION_HOURS.get(req_low, 70)
                total_hours_needed += needed_hrs

                item = {
                    **skill_info,
                    "current_proficiency": "None",
                    "status": "Missing",
                    "estimated_hours": needed_hrs
                }

                if cs.skill_type == "essential":
                    missing_essential.append(item)
                elif cs.skill_type == "preferred":
                    missing_preferred.append(item)
                else:
                    missing_additional.append(item)

        total_essential = len(acquired_essential) + len(missing_essential)
        total_preferred = len(acquired_preferred) + len(missing_preferred)
        total_additional = len(acquired_additional) + len(missing_additional)
        total_skills_count = total_essential + total_preferred + total_additional

        # Readiness percentage
        ess_ratio = (essential_score_sum / total_essential) if total_essential else 1.0
        pref_ratio = (len(acquired_preferred) / total_preferred) if total_preferred else 1.0
        add_ratio = (len(acquired_additional) / total_additional) if total_additional else 1.0

        readiness_pct = round(((0.70 * ess_ratio) + (0.20 * pref_ratio) + (0.10 * add_ratio)) * 100, 1)

        # Timeline estimation
        estimated_weeks = math.ceil(total_hours_needed / weekly_hours) if total_hours_needed > 0 else 0
        estimated_months = round(estimated_weeks / 4.3, 1)

        # High priority missing: Essential skills missing
        high_priority = missing_essential
        # Medium priority: Essential skills needing upgrade + Preferred skills missing
        medium_priority = [u for u in proficiency_upgrades if any(e["skill_id"] == u["skill_id"] for e in acquired_essential)] + missing_preferred
        # Low priority: Additional missing skills
        low_priority = missing_additional

        # Actionable bridging advice
        actionable_advice = []
        if high_priority:
            actionable_advice.append(
                f"Immediate Focus (Weeks 1-{min(8, max(2, math.ceil(len(high_priority)*2.5)))}): "
                f"Master core essential prerequisites: {', '.join([s['name'] for s in high_priority[:3]])}."
            )
        if proficiency_upgrades:
            actionable_advice.append(
                f"Proficiency Advancement: Deepen hands-on practical experience in "
                f"{', '.join([u['name'] for u in proficiency_upgrades[:3]])} to reach expected industry level."
            )
        if medium_priority and not high_priority:
            actionable_advice.append(
                f"Competitive Edge: Complement your foundation by learning preferred frameworks like "
                f"{', '.join([s['name'] for s in missing_preferred[:2]])}."
            )
        if not high_priority and not proficiency_upgrades:
            actionable_advice.append(
                "Readiness Milestone: You already meet all primary technical prerequisites! "
                "Focus on building capstone portfolio projects and practicing behavioral interviews."
            )

        return {
            "career_id": career.career_id,
            "career_code": career.career_code,
            "title": career.title,
            "category_name": career.category.name,
            "subcategory": career.subcategory,
            "description": career.description,
            "difficulty_level": career.difficulty_level,
            "entry_level_suitability": career.entry_level_suitability,
            "required_education": career.required_education,
            "preferred_education": career.preferred_education,
            "relevant_branches": career.relevant_branches,
            "soft_skills": career.soft_skills,
            "recommended_certifications": career.recommended_certifications,
            "readiness_percentage": readiness_pct,
            "total_skills_count": total_skills_count,
            "acquired_count": len(acquired_essential) + len(acquired_preferred) + len(acquired_additional),
            "missing_count": len(missing_essential) + len(missing_preferred) + len(missing_additional),
            "upgrades_needed_count": len(proficiency_upgrades),
            "acquired_essential": acquired_essential,
            "missing_essential": missing_essential,
            "acquired_preferred": acquired_preferred,
            "missing_preferred": missing_preferred,
            "acquired_additional": acquired_additional,
            "missing_additional": missing_additional,
            "high_priority_missing": high_priority,
            "medium_priority_missing": medium_priority,
            "low_priority_missing": low_priority,
            "proficiency_upgrades": proficiency_upgrades,
            "estimated_hours_needed": total_hours_needed,
            "weekly_study_hours": weekly_hours,
            "estimated_weeks_needed": estimated_weeks,
            "estimated_months_needed": estimated_months,
            "actionable_advice": actionable_advice
        }
