from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models.entities import CareerRole

class CareerService:
    @staticmethod
    def get_all(db: Session) -> List[CareerRole]:
        return db.query(CareerRole).all()

    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[CareerRole]:
        return db.query(CareerRole).filter(CareerRole.slug == slug).first()

    @staticmethod
    def get_by_id(db: Session, role_id: int) -> Optional[CareerRole]:
        return db.query(CareerRole).filter(CareerRole.id == role_id).first()

    @staticmethod
    def create_or_update(db: Session, role_data: dict) -> CareerRole:
        slug = role_data.get("slug")
        role = db.query(CareerRole).filter(CareerRole.slug == slug).first()
        if role:
            for key, val in role_data.items():
                setattr(role, key, val)
        else:
            role = CareerRole(**role_data)
            db.add(role)
        db.commit()
        db.refresh(role)
        return role
