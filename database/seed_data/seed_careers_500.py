# database/seed_data/seed_careers_500.py
"""
Large-Scale Career Knowledge Base Generator & Seeder.
Target: 500+ distinct, meaningful, specialized career profiles across 50 career families.
Maps essential (70%), preferred (20%), and additional (10%) skills, proficiency levels,
related interests, daily duties, education, recommended projects, certifications,
and junior/mid/senior career progression pathways.
"""
import os
import sys
import re

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from database.connection import get_db_session, init_db
from database.models import (
    CareerCategory, Career, CareerSkill, CareerInterest,
    TechnicalSkill, AreaOfInterest
)

from database.seed_data.careers.careers_pack_1 import PACK_1_FAMILIES
from database.seed_data.careers.careers_pack_2 import PACK_2_FAMILIES
from database.seed_data.careers.careers_pack_3 import PACK_3_FAMILIES
from database.seed_data.careers.careers_pack_4 import PACK_4_FAMILIES
from database.seed_data.careers.careers_pack_5 import PACK_5_FAMILIES

CAREER_FAMILIES = (
    PACK_1_FAMILIES +
    PACK_2_FAMILIES +
    PACK_3_FAMILIES +
    PACK_4_FAMILIES +
    PACK_5_FAMILIES
)

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[\s/\\+]+', '-', text)
    text = re.sub(r'[^a-z0-9\-._]', '', text)
    return text.strip('-')

def seed_all_careers_500(db: Session = None):
    init_db()

    def _execute(session: Session):
        total_careers = 0
        total_families = 0
        total_skills_mapped = 0
        total_interests_mapped = 0

        # Pre-cache skills and interests for rapid in-memory matching
        all_skills = session.query(TechnicalSkill).all()
        skill_by_name = {s.name: s for s in all_skills}
        skill_by_lower = {s.name.lower(): s for s in all_skills}
        skill_by_code = {s.skill_code: s for s in all_skills}

        all_interests = session.query(AreaOfInterest).all()
        interest_by_name = {i.name: i for i in all_interests}
        interest_by_lower = {i.name.lower(): i for i in all_interests}
        interest_by_code = {i.interest_code: i for i in all_interests}

        def find_skill(s_name: str):
            if not s_name:
                return None
            if s_name in skill_by_name:
                return skill_by_name[s_name]
            s_low = s_name.lower().strip()
            if s_low in skill_by_lower:
                return skill_by_lower[s_low]
            if s_name in skill_by_code:
                return skill_by_code[s_name]
            # Partial match fallback
            for s in all_skills:
                if s_low in s.name.lower() or s.name.lower() in s_low:
                    return s
            return None

        def find_interest(i_name: str):
            if not i_name:
                return None
            if i_name in interest_by_name:
                return interest_by_name[i_name]
            i_low = i_name.lower().strip()
            if i_low in interest_by_lower:
                return interest_by_lower[i_low]
            if i_name in interest_by_code:
                return interest_by_code[i_name]
            for i in all_interests:
                if i_low in i.name.lower() or i.name.lower() in i_low:
                    return i
            return None

        print(f"[*] Starting Career Seeding: {len(CAREER_FAMILIES)} families with {sum(len(f[3]) for f in CAREER_FAMILIES)} specialized career profiles...")

        for fam_code, fam_name, fam_desc, careers_list in CAREER_FAMILIES:
            # 1. Upsert Career Category
            category = session.query(CareerCategory).filter_by(code=fam_code).first()
            if not category:
                category = CareerCategory(
                    code=fam_code,
                    name=fam_name,
                    description=fam_desc
                )
                session.add(category)
                session.flush()
                total_families += 1

            # 2. Upsert Careers in this Family
            for (
                title, subcat, desc, duties,
                req_edu, pref_edu, branches,
                ess_skills, pref_skills, add_skills,
                prof, soft_skills, certs,
                diff, entry_suit, jr_roles, mid_roles, sr_roles,
                interests, industries
            ) in careers_list:
                career = session.query(Career).filter_by(title=title).first()
                if not career:
                    career = Career(
                        career_code=f"{slugify(fam_code)}-{slugify(title)[:20]}",
                        category_id=category.category_id,
                        title=title,
                        subcategory=subcat,
                        description=desc,
                        daily_responsibilities=duties,
                        required_education=req_edu,
                        preferred_education=pref_edu,
                        relevant_branches=branches,
                        soft_skills=soft_skills,
                        recommended_certifications=certs,
                        difficulty_level=diff,
                        entry_level_suitability=entry_suit,
                        junior_roles=jr_roles,
                        mid_roles=mid_roles,
                        senior_roles=sr_roles,
                        career_progression=f"Junior: {jr_roles} -> Mid: {mid_roles} -> Senior: {sr_roles}",
                        industry_sectors=industries,
                        verification_status="verified",
                        source="industry_standards"
                    )
                    session.add(career)
                    session.flush()
                    total_careers += 1

                    # Map Essential Skills (70% weight, weight=1.0)
                    seen_skills = set()
                    for s_name in ess_skills:
                        sk = find_skill(s_name)
                        if sk and sk.skill_id not in seen_skills:
                            seen_skills.add(sk.skill_id)
                            session.add(CareerSkill(
                                career_id=career.career_id,
                                skill_id=sk.skill_id,
                                skill_type="essential",
                                required_proficiency=prof,
                                importance_weight=1.0
                            ))
                            total_skills_mapped += 1

                    # Map Preferred Skills (20% weight, weight=0.6)
                    for s_name in pref_skills:
                        sk = find_skill(s_name)
                        if sk and sk.skill_id not in seen_skills:
                            seen_skills.add(sk.skill_id)
                            session.add(CareerSkill(
                                career_id=career.career_id,
                                skill_id=sk.skill_id,
                                skill_type="preferred",
                                required_proficiency=prof,
                                importance_weight=0.6
                            ))
                            total_skills_mapped += 1

                    # Map Additional Skills (10% weight, weight=0.3)
                    for s_name in add_skills:
                        sk = find_skill(s_name)
                        if sk and sk.skill_id not in seen_skills:
                            seen_skills.add(sk.skill_id)
                            session.add(CareerSkill(
                                career_id=career.career_id,
                                skill_id=sk.skill_id,
                                skill_type="additional",
                                required_proficiency=prof,
                                importance_weight=0.3
                            ))
                            total_skills_mapped += 1

                    # Map Related Interests
                    seen_interests = set()
                    for i_name in interests:
                        intr = find_interest(i_name)
                        if intr and intr.interest_id not in seen_interests:
                            seen_interests.add(intr.interest_id)
                            session.add(CareerInterest(
                                career_id=career.career_id,
                                interest_id=intr.interest_id,
                                relevance_weight=1.0
                            ))
                            total_interests_mapped += 1

        session.commit()
        return total_careers, total_families, total_skills_mapped, total_interests_mapped

    if db is not None:
        return _execute(db)
    else:
        with get_db_session() as session:
            return _execute(session)

if __name__ == "__main__":
    c_count, f_count, sk_mapped, i_mapped = seed_all_careers_500()
    print(f"\n[CAREERS SUCCESS] Seeded {c_count} distinct career profiles across {f_count} career families!")
    print(f"[RELATIONSHIPS] Mapped {sk_mapped} Career-Skill relationships and {i_mapped} Career-Interest relationships!")
