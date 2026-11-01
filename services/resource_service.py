# services/resource_service.py
"""
Curated Learning Resources Service.
Provides access to verified courses, official documentation, open access textbooks,
and interactive tutorials without fabricated URLs.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from database.models import LearningResource, Career, TechnicalSkill

class ResourceService:
    @staticmethod
    def get_resources_for_career(session: Session, career_id: int) -> List[Dict[str, Any]]:
        resources = session.query(LearningResource).filter_by(career_id=career_id, is_active=True).all()
        return [ResourceService._serialize(r) for r in resources]

    @staticmethod
    def get_resources_for_skill(session: Session, skill_id: int) -> List[Dict[str, Any]]:
        resources = session.query(LearningResource).filter_by(skill_id=skill_id, is_active=True).all()
        return [ResourceService._serialize(r) for r in resources]

    @staticmethod
    def get_all_resources(
        session: Session,
        search_query: Optional[str] = None,
        free_only: bool = False,
        resource_type: Optional[str] = None,
        difficulty: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        query = session.query(LearningResource).filter_by(is_active=True)
        if free_only:
            query = query.filter(LearningResource.is_free == True)
        if resource_type:
            query = query.filter(LearningResource.resource_type.ilike(f"%{resource_type}%"))
        if difficulty:
            query = query.filter(LearningResource.difficulty.ilike(f"%{difficulty}%"))
        if search_query:
            term = f"%{search_query}%"
            query = query.filter(
                (LearningResource.title.ilike(term)) |
                (LearningResource.provider.ilike(term))
            )
        
        resources = query.offset(offset).limit(limit).all()
        return [ResourceService._serialize(r) for r in resources]

    @staticmethod
    def _serialize(res: LearningResource) -> Dict[str, Any]:
        return {
            "resource_id": res.resource_id,
            "title": res.title,
            "provider": res.provider,
            "url": res.url,
            "career_id": res.career_id,
            "career_title": res.career.title if res.career else "General",
            "skill_id": res.skill_id,
            "skill_name": res.skill.name if res.skill else "General Technology",
            "resource_type": res.resource_type,
            "difficulty": res.difficulty,
            "is_free": res.is_free,
            "language": res.language,
            "verification_status": res.verification_status,
            "last_verified": res.last_verified
        }
