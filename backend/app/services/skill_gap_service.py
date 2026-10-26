from typing import List, Dict, Any, Set
from backend.app.models.entities import StudentProfile, CareerRole
from backend.app.schemas.career_schemas import SkillGapResponse, SkillGapItem

class SkillGapService:
    DISCLAIMER = (
        "Educational Note: Skills categorized as 'confirmed' or 'unreported' are based strictly "
        "on your self-reported profile. This analysis highlights curriculum alignment rather than "
        "independent industry assessment or employment guarantee."
    )

    # Conceptual partial match dictionary (foundations that partially cover advanced topics)
    FOUNDATION_MAP = {
        "python": ["scikit-learn", "pandas", "fastapi", "numpy", "pytorch", "tensorflow"],
        "sql": ["advanced sql", "postgresql", "data warehousing", "database design"],
        "machine learning": ["deep learning", "model evaluation", "feature engineering"],
        "docker": ["kubernetes", "ci/cd pipelines", "mlops"],
        "javascript": ["react", "typescript", "full-stack web development"]
    }

    @classmethod
    def analyze_gap(cls, student: StudentProfile, role: CareerRole) -> SkillGapResponse:
        student_skills = [s.strip().lower() for s in (student.technical_skills or [])]
        student_skill_set = set(student_skills)

        confirmed: List[str] = []
        partial: List[str] = []
        unreported: List[str] = []
        detailed_items: List[SkillGapItem] = []

        all_target_skills = []
        for s in (role.required_skills or []):
            all_target_skills.append((s, "core"))
        for s in (role.recommended_skills or []):
            all_target_skills.append((s, "recommended"))

        for skill_name, category in all_target_skills:
            norm_name = skill_name.strip().lower()

            # 1. Exact or direct substring match
            is_confirmed = False
            for s in student_skill_set:
                if norm_name in s or s in norm_name:
                    is_confirmed = True
                    break

            if is_confirmed:
                confirmed.append(skill_name)
                detailed_items.append(
                    SkillGapItem(
                        skill=skill_name,
                        category=category,
                        status="confirmed",
                        priority=3,
                        prerequisites=[]
                    )
                )
                continue

            # 2. Check partial foundation match
            is_partial = False
            for base_skill, advanced_list in cls.FOUNDATION_MAP.items():
                if base_skill in student_skill_set:
                    if any(norm_name in adv or adv in norm_name for adv in advanced_list):
                        is_partial = True
                        break

            if is_partial:
                partial.append(skill_name)
                detailed_items.append(
                    SkillGapItem(
                        skill=skill_name,
                        category=category,
                        status="partial",
                        priority=2 if category == "core" else 3,
                        prerequisites=[p for p in role.prerequisites if p]
                    )
                )
            else:
                unreported.append(skill_name)
                detailed_items.append(
                    SkillGapItem(
                        skill=skill_name,
                        category=category,
                        status="unreported",
                        priority=1 if category == "core" else 2,
                        prerequisites=[p for p in role.prerequisites if p]
                    )
                )

        # Learning order: Core unreported -> Core partial -> Recommended unreported -> Recommended partial
        ordered_skills = sorted(detailed_items, key=lambda x: (x.priority, 0 if x.category == "core" else 1))
        learning_order = [item.skill for item in ordered_skills if item.status != "confirmed"]

        return SkillGapResponse(
            career_role_title=role.title,
            career_role_slug=role.slug,
            total_required_skills=len(all_target_skills),
            confirmed_skills=confirmed,
            partially_developed_skills=partial,
            not_yet_reported_skills=unreported,
            detailed_skills=detailed_items,
            recommended_learning_order=learning_order,
            disclaimer=cls.DISCLAIMER
        )
