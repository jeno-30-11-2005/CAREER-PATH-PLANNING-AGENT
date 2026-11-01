# services/project_service.py
"""
Practical Portfolio Project Service.
Manages practical portfolio projects, implementation guides,
suggested technologies, and mapped skill relationships.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from database.models import Project, ProjectSkill, Career, TechnicalSkill

class ProjectService:
    @staticmethod
    def get_projects_for_career(session: Session, career_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves all practical projects mapped to a specific career.
        """
        projects = session.query(Project).filter_by(career_id=career_id).all()
        return [ProjectService._serialize_project(p) for p in projects]

    @staticmethod
    def get_all_projects(
        session: Session,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Queries and filters portfolio projects across all career families.
        """
        query = session.query(Project).join(Career)
        if category:
            query = query.filter(Project.category.ilike(f"%{category}%"))
        if difficulty:
            query = query.filter(Project.difficulty.ilike(f"%{difficulty}%"))
        if search_query:
            term = f"%{search_query}%"
            query = query.filter(
                (Project.title.ilike(term)) |
                (Project.suggested_technologies.ilike(term)) |
                (Project.description.ilike(term))
            )
        
        projects = query.offset(offset).limit(limit).all()
        return [ProjectService._serialize_project(p) for p in projects]

    @staticmethod
    def get_project_details(session: Session, project_id: int) -> Optional[Dict[str, Any]]:
        project = session.query(Project).filter_by(project_id=project_id).first()
        if not project:
            return None
        return ProjectService._serialize_project(project)

    @staticmethod
    def _serialize_project(project: Project) -> Dict[str, Any]:
        return {
            "project_id": project.project_id,
            "title": project.title,
            "career_id": project.career_id,
            "career_title": project.career.title if project.career else "General",
            "category": project.category,
            "difficulty": project.difficulty,
            "estimated_hours": project.estimated_hours,
            "project_type": project.project_type,
            "problem_statement": project.problem_statement,
            "objective": project.objective,
            "description": project.description,
            "suggested_technologies": project.suggested_technologies,
            "implementation_steps": project.implementation_steps,
            "expected_deliverables": project.expected_deliverables,
            "learning_outcomes": project.learning_outcomes,
            "suggested_extensions": project.suggested_extensions,
            "skills": [ps.skill.name for ps in project.skill_associations if ps.skill]
        }
