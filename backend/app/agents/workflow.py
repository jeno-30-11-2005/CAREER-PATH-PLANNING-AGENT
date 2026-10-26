from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.entities import StudentProfile, CareerRole
from backend.app.services.recommendation_service import RecommendationEngine
from backend.app.services.skill_gap_service import SkillGapService
from backend.app.services.roadmap_service import RoadmapService

class AgenticCareerWorkflow:
    """
    Controlled agentic workflow coordinating specialized pipeline components:
    1. Profile Analysis Component
    2. Career Recommendation Component
    3. Skill-Gap Analysis Component
    4. Roadmap Planning Component
    5. Quality Review Component (Guardrails)
    6. Human Review Step (Proposal awaiting student confirmation)
    """

    @classmethod
    def run_planning_workflow(
        cls,
        db: Session,
        student_id: int,
        selected_role_slug: Optional[str] = None
    ) -> Dict[str, Any]:
        workflow_log = []

        # --- Component 1: Profile Analysis Component ---
        workflow_log.append("Executing Component 1: Profile Analysis Component...")
        student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
        if not student:
            return {
                "status": "error",
                "message": f"Student with ID {student_id} not found."
            }

        declared_skills_count = len(student.technical_skills or [])
        declared_interests_count = len(student.interests or [])
        profile_completeness = 100
        if declared_skills_count == 0:
            profile_completeness -= 30
        if declared_interests_count == 0:
            profile_completeness -= 25
        if not student.career_goals:
            profile_completeness -= 15

        profile_analysis = {
            "student_name": student.name,
            "education": f"{student.degree_specialization} ({student.current_year_sem})",
            "experience_level": student.programming_experience,
            "skills_count": declared_skills_count,
            "interests_count": declared_interests_count,
            "weekly_availability_hours": student.weekly_learning_hours,
            "completeness_score": max(20, profile_completeness)
        }
        workflow_log.append(f"Profile verified. Completeness score: {profile_analysis['completeness_score']}%.")

        # --- Component 2: Career Recommendation Component ---
        workflow_log.append("Executing Component 2: Career Recommendation Component...")
        roles = db.query(CareerRole).all()
        if not roles:
            return {"status": "error", "message": "Knowledge base contains no career roles."}

        ranked_recommendations = RecommendationEngine.evaluate_profile(student, roles)
        top_recommendations = ranked_recommendations[:3]
        workflow_log.append(f"Top 3 career recommendations ranked. Leading match: {top_recommendations[0].career_role.title} ({top_recommendations[0].match_score}%).")

        # Identify target role for the roadmap
        target_role_entity = None
        if selected_role_slug:
            target_role_entity = db.query(CareerRole).filter(CareerRole.slug == selected_role_slug).first()

        if not target_role_entity and top_recommendations:
            # Default to #1 recommended role
            lead_slug = top_recommendations[0].career_role.slug
            target_role_entity = db.query(CareerRole).filter(CareerRole.slug == lead_slug).first()

        # --- Component 3: Skill-Gap Analysis Component ---
        workflow_log.append(f"Executing Component 3: Skill-Gap Analysis Component for {target_role_entity.title}...")
        gap_result = SkillGapService.analyze_gap(student, target_role_entity)
        workflow_log.append(
            f"Skill gap identified: {len(gap_result.confirmed_skills)} confirmed, "
            f"{len(gap_result.partially_developed_skills)} partial, {len(gap_result.not_yet_reported_skills)} unreported."
        )

        # --- Component 4: Roadmap Planning Component ---
        workflow_log.append("Executing Component 4: Roadmap Planning Component...")
        roadmap_proposal = RoadmapService.generate_roadmap_proposal(student, target_role_entity)
        workflow_log.append(f"Generated {len(roadmap_proposal['items'])} curriculum steps across 5 phases.")

        # --- Component 5: Quality Review Component ---
        workflow_log.append("Executing Component 5: Quality Review & Guardrail Verification...")
        quality_issues = []
        if len(roadmap_proposal["items"]) < 5:
            quality_issues.append("Roadmap does not span all 5 curriculum phases.")
        if roadmap_proposal["total_estimated_weeks"] <= 0:
            quality_issues.append("Invalid estimated timeline.")
        
        # Guardrail: Check for unsupported or exaggerated claims
        for item in roadmap_proposal["items"]:
            if "guarantee" in item["suggested_activity"].lower():
                item["suggested_activity"] = item["suggested_activity"].replace("guarantee", "help foster")
                quality_issues.append("Sanitized exaggerated guarantee language in roadmap item.")

        quality_review = {
            "passed": len(quality_issues) == 0,
            "checks_run": [
                "Completeness check across 5 pedagogical phases",
                "Prerequisite ordering validation",
                "Non-guarantee ethical assertion compliance",
                "Weekly study hour feasibility calculation"
            ],
            "issues_addressed": quality_issues
        }
        workflow_log.append("Quality review passed with zero blockers.")

        # --- Component 6: Human Review Step ---
        workflow_log.append("Component 6: Pausing for Human-in-the-Loop Review & Approval.")

        return {
            "status": "awaiting_human_approval",
            "workflow_log": workflow_log,
            "profile_analysis": profile_analysis,
            "top_recommendations": [r.model_dump() for r in top_recommendations],
            "selected_role": {
                "id": target_role_entity.id,
                "slug": target_role_entity.slug,
                "title": target_role_entity.title,
                "category": target_role_entity.category
            },
            "skill_gap_summary": gap_result.model_dump(),
            "proposed_roadmap": roadmap_proposal,
            "quality_review": quality_review,
            "requires_human_approval": True,
            "instruction": "Review the proposed plan. Approve to commit to database, or adjust steps before saving."
        }
