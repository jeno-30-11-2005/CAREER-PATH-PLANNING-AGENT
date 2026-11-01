# services/roadmap_service.py
"""
Personalized 8-Stage Learning Roadmap Generator.
Calculates realistic milestones and study schedules based on:
- Target career requirements and missing skills
- Student's available weekly study hours
- Practical portfolio project integration
"""
import math
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from database.models import (
    Career, LearningRoadmap, RoadmapItem, Student, TechnicalSkill
)

STAGE_DEFINITIONS = [
    {
        "stage": 1,
        "name": "Foundational Prerequisites & Environment Setup",
        "description": "Establish core language syntax, version control with Git, and local developer environment tooling.",
        "milestone": "Setup local development environment with Git repo and complete fundamental coding syntax challenges."
    },
    {
        "stage": 2,
        "name": "Core Technical Frameworks & Libraries",
        "description": "Master the primary frameworks, packages, and idiomatic patterns required for the career.",
        "milestone": "Build two guided mini-applications utilizing the primary framework ecosystem."
    },
    {
        "stage": 3,
        "name": "Data Persistence, APIs & Architecture",
        "description": "Learn relational or NoSQL database modeling, query optimization, and REST/GraphQL API integration.",
        "milestone": "Design and execute a normalized database schema connected to authenticated CRUD API endpoints."
    },
    {
        "stage": 4,
        "name": "Intermediate Architecture & Clean Engineering",
        "description": "Apply design patterns, modular boundaries, error handling, and automated unit testing.",
        "milestone": "Refactor application code using clean architecture patterns with >80% automated unit test coverage."
    },
    {
        "stage": 5,
        "name": "Advanced Domain Specialization & Performance",
        "description": "Deep-dive into performance tuning, caching, memory optimization, and domain-specific challenges.",
        "milestone": "Profile application latency, eliminate compute bottlenecks, and integrate distributed caching."
    },
    {
        "stage": 6,
        "name": "Full-Scale Capstone Portfolio Project",
        "description": "Synthesize all competencies into a standalone, production-grade showcase project.",
        "milestone": "Complete end-to-end implementation of an industry-standard portfolio capstone project."
    },
    {
        "stage": 7,
        "name": "Containerization, CI/CD & Cloud Deployment",
        "description": "Dockerize the solution, configure automated build/test pipelines, and deploy live on cloud infrastructure.",
        "milestone": "Deploy containerized capstone application with live URL, HTTPS, and automated GitHub Actions CI/CD."
    },
    {
        "stage": 8,
        "name": "Placement Readiness, Interview Prep & System Design",
        "description": "Prepare for technical interviews, practice behavioral questions, and polish resume highlights.",
        "milestone": "Complete mock technical coding assessments, system design interviews, and publish GitHub portfolio."
    }
]

class RoadmapService:
    @staticmethod
    def generate_roadmap(
        session: Session,
        career_id: int,
        student_profile: Dict[str, Any],
        persist: bool = False
    ) -> Dict[str, Any]:
        """
        Generates an 8-stage personalized roadmap calculated from the student's study capacity.
        """
        career = session.query(Career).filter_by(career_id=career_id).first()
        if not career:
            raise ValueError(f"Career with ID {career_id} not found.")

        weekly_hours = max(5, int(student_profile.get("weekly_learning_hours", 15)))

        # Collect career skills
        essential_names = [cs.skill.name for cs in career.skills if cs.skill_type == "essential"]
        preferred_names = [cs.skill.name for cs in career.skills if cs.skill_type == "preferred"]
        additional_names = [cs.skill.name for cs in career.skills if cs.skill_type == "additional"]

        # Difficulty multiplier
        diff = (career.difficulty_level or "Intermediate").lower()
        if "advanced" in diff:
            base_hours_per_stage = 40
        elif "beginner" in diff:
            base_hours_per_stage = 25
        else:
            base_hours_per_stage = 32

        stages = []
        total_hours = 0

        for defn in STAGE_DEFINITIONS:
            stg_num = defn["stage"]
            stg_hours = base_hours_per_stage

            # Assign topic focus
            if stg_num == 1:
                topic = f"Git, Version Control & Foundation Prerequisite Syntax"
                stg_hours = round(base_hours_per_stage * 0.8)
            elif stg_num == 2:
                topic = f"Core Essential Tech: {', '.join(essential_names[:2]) if essential_names else 'Core Frameworks'}"
                stg_hours = round(base_hours_per_stage * 1.1)
            elif stg_num == 3:
                topic = f"Data & Integration: {essential_names[2] if len(essential_names) > 2 else 'Database & Storage'}"
                stg_hours = base_hours_per_stage
            elif stg_num == 4:
                topic = f"Architecture & Testing for {career.title}"
                stg_hours = base_hours_per_stage
            elif stg_num == 5:
                topic = f"Advanced Competencies: {', '.join(preferred_names[:2]) if preferred_names else 'Domain Mastery'}"
                stg_hours = round(base_hours_per_stage * 1.2)
            elif stg_num == 6:
                topic = f"Portfolio Capstone Project: Production {career.title} Application"
                stg_hours = round(base_hours_per_stage * 1.4)
            elif stg_num == 7:
                topic = f"Docker, CI/CD & Cloud Deployment"
                stg_hours = round(base_hours_per_stage * 0.9)
            else:
                topic = f"Technical Interview Preparation & {career.title} Case Studies"
                stg_hours = round(base_hours_per_stage * 0.8)

            total_hours += stg_hours
            stg_weeks = max(1, math.ceil(stg_hours / weekly_hours))

            stages.append({
                "stage_number": stg_num,
                "stage_name": defn["name"],
                "topic_title": topic,
                "description": defn["description"],
                "milestone": defn["milestone"],
                "estimated_hours": stg_hours,
                "estimated_weeks": stg_weeks,
                "is_completed": False
            })

        total_weeks = math.ceil(total_hours / weekly_hours)
        total_months = round(total_weeks / 4.3, 1)

        result = {
            "career_id": career.career_id,
            "career_title": career.title,
            "category_name": career.category.name,
            "difficulty_level": career.difficulty_level,
            "weekly_study_hours": weekly_hours,
            "total_stages": len(stages),
            "total_hours": total_hours,
            "estimated_total_weeks": total_weeks,
            "estimated_total_months": total_months,
            "stages": stages
        }

        # Optional persistence for registered students
        student_id = student_profile.get("student_id")
        if persist and student_id:
            # Check existing roadmap
            existing = session.query(LearningRoadmap).filter_by(
                student_id=student_id, career_id=career_id
            ).first()
            if not existing:
                rd = LearningRoadmap(
                    student_id=student_id,
                    career_id=career_id,
                    title=f"8-Stage Personalized Roadmap for {career.title}",
                    total_stages=len(stages),
                    weekly_hours=weekly_hours,
                    estimated_total_weeks=total_weeks
                )
                session.add(rd)
                session.flush()

                for item in stages:
                    session.add(RoadmapItem(
                        roadmap_id=rd.roadmap_id,
                        stage_number=item["stage_number"],
                        stage_name=item["stage_name"],
                        topic_title=item["topic_title"],
                        description=item["description"],
                        milestone=item["milestone"],
                        estimated_hours=item["estimated_hours"],
                        is_completed=False
                    ))
                session.commit()
                result["roadmap_id"] = rd.roadmap_id

        return result
