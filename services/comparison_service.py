# services/comparison_service.py
"""
Career Comparison Engine.
Compares 2 or 3 career profiles side-by-side across:
- Essential & preferred skill requirements
- Common skill overlap vs. distinct domain requirements
- Educational prerequisites & difficulty levels
- Career progression ladders and industry applications
- Student compatibility comparison
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from database.models import Career, TechnicalSkill
from services.recommendation_service import RecommendationEngine

class CareerComparisonService:
    @staticmethod
    def compare_careers(
        session: Session,
        career_ids: List[int],
        student_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates a structured side-by-side comparison for 2 to 3 careers.
        """
        if len(career_ids) < 2 or len(career_ids) > 3:
            raise ValueError("Comparison requires between 2 and 3 careers.")

        careers = session.query(Career).filter(Career.career_id.in_(career_ids)).all()
        if len(careers) != len(career_ids):
            raise ValueError("One or more selected careers were not found.")

        # Re-order to match input sequence
        career_map = {c.career_id: c for c in careers}
        ordered_careers = [career_map[cid] for cid in career_ids]

        # Extract skill sets
        career_skill_sets = []
        for c in ordered_careers:
            ess = {cs.skill.name for cs in c.skills if cs.skill and cs.skill_type == "essential"}
            pref = {cs.skill.name for cs in c.skills if cs.skill and cs.skill_type == "preferred"}
            career_skill_sets.append({
                "essential": ess,
                "preferred": pref,
                "all": ess.union(pref)
            })

        # Calculate common skills across all compared careers
        common_essential = set.intersection(*[s["essential"] for s in career_skill_sets])
        common_all = set.intersection(*[s["all"] for s in career_skill_sets])

        # Student compatibility if profile provided
        student_scores = {}
        if student_profile:
            recs = RecommendationEngine.get_recommendations(
                session, student_profile, top_k=500
            )
            rec_map = {r["career_id"]: r for r in recs}
            for c in ordered_careers:
                if c.career_id in rec_map:
                    student_scores[c.career_id] = rec_map[c.career_id]["compatibility_score"]

        comparison_data = []
        for idx, c in enumerate(ordered_careers):
            all_career_skills = career_skill_sets[idx]["all"]
            other_skills = set.union(*[
                career_skill_sets[j]["all"] for j in range(len(ordered_careers)) if j != idx
            ])
            unique_to_this = all_career_skills - other_skills

            comparison_data.append({
                "career_id": c.career_id,
                "title": c.title,
                "category": c.category.name,
                "subcategory": c.subcategory,
                "description": c.description,
                "daily_responsibilities": c.daily_responsibilities,
                "difficulty_level": c.difficulty_level,
                "entry_level_suitability": c.entry_level_suitability,
                "required_education": c.required_education,
                "preferred_education": c.preferred_education,
                "relevant_branches": c.relevant_branches,
                "soft_skills": c.soft_skills,
                "recommended_certifications": c.recommended_certifications,
                "career_progression": c.career_progression,
                "junior_roles": c.junior_roles,
                "mid_roles": c.mid_roles,
                "senior_roles": c.senior_roles,
                "industry_sectors": c.industry_sectors,
                "essential_skills": sorted(list(career_skill_sets[idx]["essential"])),
                "preferred_skills": sorted(list(career_skill_sets[idx]["preferred"])),
                "unique_skills": sorted(list(unique_to_this)),
                "student_compatibility": student_scores.get(c.career_id)
            })

        return {
            "careers": comparison_data,
            "common_essential_skills": sorted(list(common_essential)),
            "common_all_skills": sorted(list(common_all)),
            "comparison_summary": CareerComparisonService._generate_summary(comparison_data)
        }

    @staticmethod
    def _generate_summary(comparison_data: List[Dict[str, Any]]) -> str:
        titles = [c["title"] for c in comparison_data]
        if len(titles) == 2:
            return (
                f"Comparing {titles[0]} and {titles[1]}: Both roles share foundational competencies "
                f"but differ in primary day-to-day duties and domain specialization. "
                f"{titles[0]} emphasizes {comparison_data[0]['subcategory']}, whereas {titles[1]} "
                f"focuses on {comparison_data[1]['subcategory']}."
            )
        else:
            return (
                f"Comparing {titles[0]}, {titles[1]}, and {titles[2]}: "
                f"Review the overlapping technical requirements and unique prerequisites below to identify "
                f"which path aligns best with your existing strengths."
            )
