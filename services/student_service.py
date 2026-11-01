# services/student_service.py
"""
Student Profile & Progress Tracking Service.
Manages student registration, skill inventories with proficiency levels,
interest mappings, target careers, and progress tracking across milestones.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database.models import (
    Student, StudentSkill, StudentInterest, StudentProgress,
    TechnicalSkill, AreaOfInterest, Career
)

class StudentService:
    @staticmethod
    def create_or_update_student(
        session: Session,
        full_name: str,
        email: str,
        academic_branch: str = "CSE",
        education_level: str = "Bachelor's",
        current_year: int = 3,
        weekly_hours: int = 15,
        target_career_id: Optional[int] = None
    ) -> Student:
        student = session.query(Student).filter_by(email=email).first()
        if not student:
            student = Student(
                full_name=full_name,
                email=email,
                academic_branch=academic_branch,
                education_level=education_level,
                current_year=current_year,
                weekly_learning_hours=weekly_hours,
                target_career_id=target_career_id
            )
            session.add(student)
        else:
            student.full_name = full_name
            student.academic_branch = academic_branch
            student.education_level = education_level
            student.current_year = current_year
            student.weekly_learning_hours = weekly_hours
            if target_career_id:
                student.target_career_id = target_career_id
        session.commit()
        return student

    @staticmethod
    def get_student_by_email(session: Session, email: str) -> Optional[Student]:
        return session.query(Student).filter_by(email=email).first()

    @staticmethod
    def get_student_profile_dict(session: Session, student_id: int) -> Optional[Dict[str, Any]]:
        student = session.query(Student).filter_by(student_id=student_id).first()
        if not student:
            return None

        # Build skill map
        skills_map = {}
        for ss in student.skills:
            if ss.skill:
                skills_map[ss.skill.skill_id] = ss.proficiency_level
            elif ss.custom_skill_name:
                skills_map[ss.custom_skill_name] = ss.proficiency_level

        # Build interests list
        interests_list = []
        for si in student.interests:
            if si.interest:
                interests_list.append(si.interest.interest_id)

        return {
            "student_id": student.student_id,
            "full_name": student.full_name,
            "email": student.email,
            "academic_branch": student.academic_branch,
            "education_level": student.education_level,
            "current_year": student.current_year,
            "weekly_learning_hours": student.weekly_learning_hours,
            "target_career_id": student.target_career_id,
            "skills": skills_map,
            "interests": interests_list
        }

    @staticmethod
    def set_student_skills(
        session: Session,
        student_id: int,
        skills_with_proficiency: Dict[int, str]
    ):
        """
        Replaces student's active skills with the provided dictionary (skill_id -> proficiency).
        """
        session.query(StudentSkill).filter_by(student_id=student_id).delete()
        for s_id, prof in skills_with_proficiency.items():
            session.add(StudentSkill(
                student_id=student_id,
                skill_id=s_id,
                proficiency_level=prof,
                is_custom=False
            ))
        session.commit()

    @staticmethod
    def set_student_interests(
        session: Session,
        student_id: int,
        interest_ids: List[int]
    ):
        session.query(StudentInterest).filter_by(student_id=student_id).delete()
        for i_id in interest_ids:
            session.add(StudentInterest(
                student_id=student_id,
                interest_id=i_id,
                is_custom=False
            ))
        session.commit()

    @staticmethod
    def update_progress(
        session: Session,
        student_id: int,
        career_id: int,
        readiness_pct: float,
        completed_skills: int,
        total_skills: int,
        completed_projects: int = 0,
        milestones_done: int = 0
    ) -> StudentProgress:
        prog = session.query(StudentProgress).filter_by(
            student_id=student_id, career_id=career_id
        ).first()

        if not prog:
            prog = StudentProgress(
                student_id=student_id,
                career_id=career_id,
                completed_skills_count=completed_skills,
                total_required_skills=total_skills,
                completed_projects_count=completed_projects,
                milestones_completed=milestones_done,
                overall_readiness_pct=readiness_pct
            )
            session.add(prog)
        else:
            prog.completed_skills_count = completed_skills
            prog.total_required_skills = total_skills
            prog.completed_projects_count = completed_projects
            prog.milestones_completed = milestones_done
            prog.overall_readiness_pct = readiness_pct
            prog.updated_at = datetime.utcnow()
        session.commit()
        return prog
