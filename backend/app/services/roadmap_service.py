from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.entities import StudentProfile, CareerRole, LearningRoadmap, RoadmapItem
from backend.app.services.skill_gap_service import SkillGapService

class RoadmapService:
    # High-quality verified learning resources (official documentation and reputable open-access hubs)
    VERIFIED_RESOURCES = {
        "Python": [
            {"title": "Official Python Tutorial", "url": "https://docs.python.org/3/tutorial/"},
            {"title": "Real Python Tutorials", "url": "https://realpython.com/"}
        ],
        "FastAPI": [
            {"title": "FastAPI Official Documentation", "url": "https://fastapi.tiangolo.com/"},
            {"title": "FastAPI Full Tutorial (MDN style)", "url": "https://fastapi.tiangolo.com/tutorial/"}
        ],
        "SQL": [
            {"title": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com/"},
            {"title": "SQLBolt Interactive Lessons", "url": "https://sqlbolt.com/"}
        ],
        "Scikit-Learn": [
            {"title": "Scikit-Learn User Guide", "url": "https://scikit-learn.org/stable/user_guide.html"},
            {"title": "ML Course by Google Developers", "url": "https://developers.google.com/machine-learning/crash-course"}
        ],
        "Docker": [
            {"title": "Docker Getting Started Guide", "url": "https://docs.docker.com/get-started/"}
        ],
        "React": [
            {"title": "React Official Docs (react.dev)", "url": "https://react.dev/"}
        ],
        "AI": [
            {"title": "Google AI for Developers Guide", "url": "https://ai.google.dev/docs"},
            {"title": "DeepLearning.AI Short Courses", "url": "https://www.deeplearning.ai/short-courses/"}
        ]
    }

    @classmethod
    def get_resource_links_for_topic(cls, topic: str) -> List[Dict[str, str]]:
        topic_lower = topic.lower()
        matched = []
        for key, links in cls.VERIFIED_RESOURCES.items():
            if key.lower() in topic_lower or topic_lower in key.lower():
                matched.extend(links)
        if not matched:
            matched.append({
                "title": f"Community & Docs for {topic}",
                "url": f"https://devdocs.io/#q={topic.replace(' ', '+')}"
            })
        return matched[:2]

    @classmethod
    def generate_roadmap_proposal(cls, student: StudentProfile, role: CareerRole) -> Dict[str, Any]:
        gap_analysis = SkillGapService.analyze_gap(student, role)
        weekly_hours = max(5, student.weekly_learning_hours or 10)

        # Build 5 phases
        items: List[Dict[str, Any]] = []
        step = 1

        # Phase 1: Foundations
        foundation_topics = role.prerequisites if role.prerequisites else ["Foundational Programming Concepts"]
        for topic in foundation_topics:
            items.append({
                "phase": "1. Foundations",
                "step_number": step,
                "skill_topic": topic,
                "why_it_matters": f"Establishes prerequisite mental models required for advanced {role.title} topics.",
                "prerequisites": ["Basic Computer Operations"],
                "suggested_activity": f"Complete foundational syntax and problem-solving modules for {topic}.",
                "estimated_effort_hours": 12,
                "practical_exercise": "Implement 3 algorithmic exercises and document solutions.",
                "milestone_project": "Core concepts cheat-sheet and verified sandbox repository.",
                "completion_status": "not_started",
                "resource_links": cls.get_resource_links_for_topic(topic)
            })
            step += 1

        # Phase 2: Core Technical Skills (Prioritize missing core skills)
        core_skills_to_learn = [
            item.skill for item in gap_analysis.detailed_skills 
            if item.category == "core" and item.status != "confirmed"
        ]
        if not core_skills_to_learn:
            core_skills_to_learn = (role.required_skills or [])[:3]

        for skill in core_skills_to_learn:
            items.append({
                "phase": "2. Core Technical Skills",
                "step_number": step,
                "skill_topic": skill,
                "why_it_matters": f"Essential skill directly demanded in industry role specifications for {role.title}.",
                "prerequisites": [foundation_topics[0] if foundation_topics else "Foundations"],
                "suggested_activity": f"Deep-dive into syntax, best practices, and standard conventions for {skill}.",
                "estimated_effort_hours": 15,
                "practical_exercise": f"Build a reproducible mini-module demonstrating {skill} without external helpers.",
                "milestone_project": f"Functional {skill} module integrated with automated tests.",
                "completion_status": "not_started",
                "resource_links": cls.get_resource_links_for_topic(skill)
            })
            step += 1

        # Phase 3: Applied Practice & Tooling
        applied_skills = (role.tools_technologies or [])[:3]
        for tool in applied_skills:
            items.append({
                "phase": "3. Applied Practice",
                "step_number": step,
                "skill_topic": f"Tooling & Practice: {tool}",
                "why_it_matters": f"Hands-on proficiency with {tool} is standard in professional {role.title} toolchains.",
                "prerequisites": ["Core Technical Skills"],
                "suggested_activity": f"Configure a development environment with {tool} and build a demo pipeline.",
                "estimated_effort_hours": 14,
                "practical_exercise": f"Connect {tool} to an active dataset or mock backend endpoint.",
                "milestone_project": f"End-to-end integration demo utilizing {tool}.",
                "completion_status": "not_started",
                "resource_links": cls.get_resource_links_for_topic(tool)
            })
            step += 1

        # Phase 4: Portfolio Projects
        portfolio_projects = role.example_projects if role.example_projects else [f"{role.title} Showcase Application"]
        for proj in portfolio_projects[:2]:
            items.append({
                "phase": "4. Portfolio Projects",
                "step_number": step,
                "skill_topic": f"Portfolio Project: {proj}",
                "why_it_matters": "Real-world projects showcase evidence of your engineering ability to college recruiters.",
                "prerequisites": ["Applied Practice", "Version Control (Git)"],
                "suggested_activity": f"Architect and code '{proj}' following modular code structure and git commits.",
                "estimated_effort_hours": 20,
                "practical_exercise": "Deploy the application to a cloud host or containerize it with Docker.",
                "milestone_project": f"Published GitHub repository with clear README, diagrams, and live demo link.",
                "completion_status": "not_started",
                "resource_links": cls.get_resource_links_for_topic(role.title)
            })
            step += 1

        # Phase 5: Interview Preparation
        items.append({
            "phase": "5. Interview Preparation",
            "step_number": step,
            "skill_topic": f"{role.title} Technical & Conceptual Viva Prep",
            "why_it_matters": "Prepares you to articulate architectural decisions, complexity, and trade-offs.",
            "prerequisites": ["Portfolio Projects"],
            "suggested_activity": f"Review standard viva questions on {role.title} workflows and conduct mock Q&A.",
            "estimated_effort_hours": 10,
            "practical_exercise": "Conduct a 20-minute timed mock interview explaining your portfolio project.",
            "milestone_project": "Completed viva revision flashcards and resume project highlight bullet points.",
            "completion_status": "not_started",
            "resource_links": [
                {"title": "Open Source Tech Interview Handbook", "url": "https://www.techinterviewhandbook.org/"}
            ]
        })

        total_hours = sum(i["estimated_effort_hours"] for i in items)
        total_weeks = max(4, round(total_hours / weekly_hours))

        return {
            "student_profile_id": student.id,
            "career_role_id": role.id,
            "title": f"Personalized {role.title} Roadmap for {student.name}",
            "target_role": role.title,
            "weekly_hours": weekly_hours,
            "total_estimated_weeks": total_weeks,
            "is_approved": False,
            "generation_method": "deterministic",
            "items": items
        }

    @classmethod
    def save_approved_roadmap(cls, db: Session, student_id: int, role_id: int, proposal_data: Dict[str, Any]) -> LearningRoadmap:
        # Check if an existing roadmap exists for this student and role
        existing = db.query(LearningRoadmap).filter(
            LearningRoadmap.student_profile_id == student_id,
            LearningRoadmap.career_role_id == role_id
        ).first()

        if existing:
            existing.title = proposal_data.get("title", existing.title)
            existing.weekly_hours = proposal_data.get("weekly_hours", existing.weekly_hours)
            existing.total_estimated_weeks = proposal_data.get("total_estimated_weeks", existing.total_estimated_weeks)
            existing.is_approved = True
            # Replace items
            existing.items.clear()
            for item_data in proposal_data.get("items", []):
                new_item = RoadmapItem(
                    phase=item_data["phase"],
                    step_number=item_data["step_number"],
                    skill_topic=item_data["skill_topic"],
                    why_it_matters=item_data["why_it_matters"],
                    prerequisites=item_data.get("prerequisites", []),
                    suggested_activity=item_data["suggested_activity"],
                    estimated_effort_hours=item_data.get("estimated_effort_hours", 10),
                    practical_exercise=item_data["practical_exercise"],
                    milestone_project=item_data["milestone_project"],
                    completion_status=item_data.get("completion_status", "not_started"),
                    resource_links=item_data.get("resource_links", []),
                    learning_notes=item_data.get("learning_notes")
                )
                existing.items.append(new_item)
            db.commit()
            db.refresh(existing)
            return existing
        else:
            roadmap = LearningRoadmap(
                student_profile_id=student_id,
                career_role_id=role_id,
                title=proposal_data.get("title", "Custom Learning Roadmap"),
                target_role=proposal_data.get("target_role", "Target Career"),
                weekly_hours=proposal_data.get("weekly_hours", 10),
                total_estimated_weeks=proposal_data.get("total_estimated_weeks", 12),
                is_approved=True,
                generation_method=proposal_data.get("generation_method", "deterministic")
            )
            for item_data in proposal_data.get("items", []):
                new_item = RoadmapItem(
                    phase=item_data["phase"],
                    step_number=item_data["step_number"],
                    skill_topic=item_data["skill_topic"],
                    why_it_matters=item_data["why_it_matters"],
                    prerequisites=item_data.get("prerequisites", []),
                    suggested_activity=item_data["suggested_activity"],
                    estimated_effort_hours=item_data.get("estimated_effort_hours", 10),
                    practical_exercise=item_data["practical_exercise"],
                    milestone_project=item_data["milestone_project"],
                    completion_status=item_data.get("completion_status", "not_started"),
                    resource_links=item_data.get("resource_links", []),
                    learning_notes=item_data.get("learning_notes")
                )
                roadmap.items.append(new_item)
            db.add(roadmap)
            db.commit()
            db.refresh(roadmap)
            return roadmap
