# services/admin_service.py
"""
Administrator & Bulk Ingestion Service.
Supports:
- Secure administrator authentication with bcrypt
- Default admin bootstrapping
- CSV and JSON bulk import with schema validation and duplicate checking
- System audit logging (DataImportLog)
- System metrics and catalog management
"""
import io
import csv
import json
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import bcrypt
from sqlalchemy.orm import Session
from database.models import (
    Administrator, DataImportLog, TechnicalSkill, SkillCategory,
    Career, CareerCategory, AreaOfInterest, InterestCategory,
    Project, LearningResource, Student
)

class AdminService:
    @staticmethod
    def ensure_default_admin(session: Session) -> Administrator:
        """
        Creates a default administrator (admin / admin123) if none exists.
        """
        admin = session.query(Administrator).filter_by(username="admin").first()
        if not admin:
            pwd_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode("utf-8")
            admin = Administrator(
                username="admin",
                password_hash=pwd_hash,
                role="SuperAdmin",
                is_active=True
            )
            session.add(admin)
            session.commit()
        return admin

    @staticmethod
    def authenticate(session: Session, username: str, password: str) -> Optional[Administrator]:
        AdminService.ensure_default_admin(session)
        admin = session.query(Administrator).filter_by(username=username, is_active=True).first()
        if not admin:
            return None
        if bcrypt.checkpw(password.encode("utf-8"), admin.password_hash.encode("utf-8")):
            return admin
        return None

    @staticmethod
    def get_system_stats(session: Session) -> Dict[str, Any]:
        """
        Gathers real-time database counts and health metrics for the admin dashboard.
        """
        return {
            "total_skills": session.query(TechnicalSkill).count(),
            "active_skills": session.query(TechnicalSkill).filter_by(is_active=True).count(),
            "skill_categories": session.query(SkillCategory).count(),
            "total_interests": session.query(AreaOfInterest).count(),
            "interest_categories": session.query(InterestCategory).count(),
            "total_careers": session.query(Career).count(),
            "career_categories": session.query(CareerCategory).count(),
            "total_projects": session.query(Project).count(),
            "total_resources": session.query(LearningResource).count(),
            "total_students": session.query(Student).count(),
            "import_logs": session.query(DataImportLog).count()
        }

    @staticmethod
    def import_skills_from_csv(
        session: Session,
        csv_content: str,
        imported_by: str = "admin"
    ) -> Dict[str, Any]:
        """
        Bulk imports technical skills from CSV with validation and duplicate prevention.
        Expected columns: name, category, subcategory, description, difficulty_level, learning_priority
        """
        reader = csv.DictReader(io.StringIO(csv_content))
        total = 0
        inserted = 0
        rejected = 0
        errors = []

        # Cache existing categories and skills
        cat_map = {c.name.lower(): c.category_id for c in session.query(SkillCategory).all()}
        existing_names = {s.name.lower() for s in session.query(TechnicalSkill.name).all()}

        for row_idx, row in enumerate(reader, 1):
            total += 1
            name = (row.get("name") or "").strip()
            category_name = (row.get("category") or "General Technology").strip()
            desc = (row.get("description") or f"Competency in {name}.").strip()
            diff = (row.get("difficulty_level") or "Intermediate").strip()
            priority = (row.get("learning_priority") or "High").strip()

            if not name:
                rejected += 1
                errors.append(f"Row {row_idx}: Skill name cannot be empty.")
                continue

            if name.lower() in existing_names:
                rejected += 1
                errors.append(f"Row {row_idx}: Skill '{name}' already exists in database (duplicate).")
                continue

            # Ensure category exists
            cat_id = cat_map.get(category_name.lower())
            if not cat_id:
                new_cat = SkillCategory(
                    code=category_name[:10].upper(),
                    name=category_name,
                    description=f"{category_name} skills domain"
                )
                session.add(new_cat)
                session.flush()
                cat_id = new_cat.category_id
                cat_map[category_name.lower()] = cat_id

            slug_code = re_slug(name)
            new_skill = TechnicalSkill(
                skill_code=f"sk-{slug_code[:40]}",
                name=name,
                category_id=cat_id,
                subcategory=row.get("subcategory", "General"),
                description=desc,
                difficulty_level=diff,
                learning_priority=priority,
                industry_relevance="High",
                is_active=True,
                verification_status="Imported",
                source="Admin Bulk Ingestion"
            )
            session.add(new_skill)
            existing_names.add(name.lower())
            inserted += 1

        # Audit Log
        log = DataImportLog(
            entity_type="TechnicalSkill",
            source_format="CSV",
            total_records=total,
            inserted_records=inserted,
            rejected_records=rejected,
            error_log="\n".join(errors[:20]),
            imported_by=imported_by
        )
        session.add(log)
        session.commit()

        return {
            "total_records": total,
            "inserted_records": inserted,
            "rejected_records": rejected,
            "errors": errors
        }

    @staticmethod
    def import_skills_from_json(
        session: Session,
        json_content: str,
        imported_by: str = "admin"
    ) -> Dict[str, Any]:
        """
        Bulk imports technical skills from JSON.
        """
        try:
            data = json.loads(json_content)
        except Exception as e:
            return {"error": f"Invalid JSON format: {str(e)}", "inserted_records": 0}

        if not isinstance(data, list):
            data = [data]

        total = len(data)
        inserted = 0
        rejected = 0
        errors = []

        cat_map = {c.name.lower(): c.category_id for c in session.query(SkillCategory).all()}
        existing_names = {s.name.lower() for s in session.query(TechnicalSkill.name).all()}

        for idx, item in enumerate(data, 1):
            name = (item.get("name") or "").strip()
            cat_name = (item.get("category") or "General Technology").strip()

            if not name:
                rejected += 1
                errors.append(f"Item {idx}: Missing 'name'")
                continue
            if name.lower() in existing_names:
                rejected += 1
                errors.append(f"Item {idx}: Duplicate skill '{name}'")
                continue

            cat_id = cat_map.get(cat_name.lower())
            if not cat_id:
                new_cat = SkillCategory(
                    code=cat_name[:10].upper(),
                    name=cat_name,
                    description=f"{cat_name} skills domain"
                )
                session.add(new_cat)
                session.flush()
                cat_id = new_cat.category_id
                cat_map[cat_name.lower()] = cat_id

            new_skill = TechnicalSkill(
                skill_code=f"sk-{re_slug(name)[:40]}",
                name=name,
                category_id=cat_id,
                subcategory=item.get("subcategory", "General"),
                description=item.get("description", f"Competency in {name}"),
                difficulty_level=item.get("difficulty_level", "Intermediate"),
                learning_priority=item.get("learning_priority", "High"),
                industry_relevance="High",
                is_active=True,
                verification_status="Imported",
                source="Admin JSON Ingestion"
            )
            session.add(new_skill)
            existing_names.add(name.lower())
            inserted += 1

        log = DataImportLog(
            entity_type="TechnicalSkill",
            source_format="JSON",
            total_records=total,
            inserted_records=inserted,
            rejected_records=rejected,
            error_log="\n".join(errors[:20]),
            imported_by=imported_by
        )
        session.add(log)
        session.commit()

        return {
            "total_records": total,
            "inserted_records": inserted,
            "rejected_records": rejected,
            "errors": errors
        }

def re_slug(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r'[\s/\\+]+', '-', text)
    text = re.sub(r'[^a-z0-9\-._]', '', text)
    return text.strip('-')
