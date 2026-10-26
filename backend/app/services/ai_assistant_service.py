from typing import Optional, Dict, Any, List
from backend.app.core.config import settings
from backend.app.models.entities import StudentProfile, CareerRole
from backend.app.db.seed_data import CAREER_ROLES_SEED

class AIAssistantService:
    @classmethod
    def generate_reply(
        cls,
        user_message: str,
        student: Optional[StudentProfile] = None,
        role: Optional[CareerRole] = None
    ) -> Dict[str, Any]:
        """
        Processes student inquiry. First attempts Gemini LLM if key is configured;
        gracefully falls back to knowledge-grounded deterministic engine if unavailable.
        """
        api_key = settings.GEMINI_API_KEY.strip() if settings.GEMINI_API_KEY else ""

        # Check if LLM is accessible
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(settings.GEMINI_MODEL)

                context_prompts = [
                    "You are the Intelligent Career Path Planning Assistant for AI & Data Science engineering students.",
                    "Ground your advice strictly in verified computer science curricula and project requirements.",
                    "Do NOT guarantee employment, job placements, or specific salaries.",
                    "Be encouraging, structured, practical, and beginner-friendly."
                ]

                if student:
                    context_prompts.append(
                        f"Student Context: {student.name}, Degree: {student.degree_specialization}, "
                        f"Year: {student.current_year_sem}, Skills: {', '.join(student.technical_skills or [])}, "
                        f"Interests: {', '.join(student.interests or [])}, Weekly Hours: {student.weekly_learning_hours}."
                    )
                if role:
                    context_prompts.append(
                        f"Target Career Context: {role.title} ({role.category}). "
                        f"Required Skills: {', '.join(role.required_skills or [])}. "
                        f"Key Tools: {', '.join(role.tools_technologies or [])}. "
                        f"Projects: {', '.join(role.example_projects or [])}."
                    )

                full_prompt = "\n".join(context_prompts) + f"\n\nStudent Question: {user_message}\nYour Response:"
                response = model.generate_content(full_prompt)

                if response and response.text:
                    return {
                        "reply": response.text.strip(),
                        "is_fallback": False,
                        "sources": ["Google Gemini 1.5 Flash", "Institutional Career Knowledge Base"]
                    }
            except Exception as e:
                # Log error and fall back cleanly
                print(f"[AIAssistantService] Gemini API invocation failed: {str(e)}. Switching to deterministic fallback.")

        # Deterministic Knowledge-Based Fallback
        return cls._deterministic_fallback_reply(user_message, student, role)

    @classmethod
    def _deterministic_fallback_reply(
        cls,
        user_message: str,
        student: Optional[StudentProfile],
        role: Optional[CareerRole]
    ) -> Dict[str, Any]:
        query = user_message.lower().strip()
        matched_role = role

        # If role not explicitly selected, try to detect role keywords in query
        if not matched_role:
            for seed in CAREER_ROLES_SEED:
                if seed["title"].lower() in query or seed["slug"] in query:
                    # Found match
                    class MockRole:
                        pass
                    m = MockRole()
                    for k, v in seed.items():
                        setattr(m, k, v)
                    matched_role = m
                    break

        sources = ["Deterministic Knowledge Base Engine", "Academic Curriculum Standards"]

        if any(w in query for w in ["salary", "job guarantee", "hire", "placement"]):
            return {
                "reply": (
                    "As an educational guidance tool, I focus strictly on helping you build technical competencies, "
                    "project portfolios, and solid conceptual foundations. I cannot guarantee specific job offers or salary packages, "
                    "as hiring outcomes depend on market conditions, company interviews, and your demonstrated engineering execution."
                ),
                "is_fallback": True,
                "sources": sources
            }

        if any(w in query for w in ["project", "idea", "portfolio"]):
            if matched_role:
                projects = matched_role.example_projects or []
                proj_bullets = "\n".join(f"- **{p}**" for p in projects)
                return {
                    "reply": (
                        f"Here are high-impact portfolio project ideas for becoming a **{matched_role.title}**:\n\n"
                        f"{proj_bullets}\n\n"
                        "💡 *Tip:* When presenting projects in your viva or campus placement, emphasize your data pipeline, "
                        "algorithmic trade-offs, and testing methodology!"
                    ),
                    "is_fallback": True,
                    "sources": sources
                }
            else:
                return {
                    "reply": (
                        "Strong AI & Data Science portfolio projects typically include:\n"
                        "1. **Predictive Machine Learning API:** End-to-end model trained in Scikit-Learn/PyTorch and deployed via FastAPI.\n"
                        "2. **Domain-Specific RAG System:** Vector search with source citations for college notes or technical docs.\n"
                        "3. **Data Pipeline (ETL):** Automated data extraction, transformation, and database storage with quality checks.\n\n"
                        "Select any career role in the recommendations tab to see specialized project roadmaps!"
                    ),
                    "is_fallback": True,
                    "sources": sources
                }

        if any(w in query for w in ["roadmap", "steps", "start", "learn first"]):
            if matched_role:
                seq = matched_role.learning_sequence or []
                seq_bullets = "\n".join(f"{s}" for s in seq)
                return {
                    "reply": (
                        f"Here is the recommended progressive learning sequence for **{matched_role.title}**:\n\n"
                        f"{seq_bullets}\n\n"
                        f"You can review and generate your full step-by-step roadmap in the Roadmap Planner module."
                    ),
                    "is_fallback": True,
                    "sources": sources
                }

        if any(w in query for w in ["skill", "tool", "stack", "require"]):
            if matched_role:
                req = ", ".join(matched_role.required_skills or [])
                rec = ", ".join(matched_role.recommended_skills or [])
                tools = ", ".join(matched_role.tools_technologies or [])
                return {
                    "reply": (
                        f"For **{matched_role.title}**, the skill framework is:\n\n"
                        f"- **Core Technical Requirements:** {req}\n"
                        f"- **Recommended Additional Skills:** {rec}\n"
                        f"- **Industry Standard Tools:** {tools}\n\n"
                        f"Check out your Skill Gap Analysis to see which of these skills you have already declared!"
                    ),
                    "is_fallback": True,
                    "sources": sources
                }

        # Default thoughtful reply
        student_greeting = f"Hello {student.name}! " if student else "Hello! "
        role_mention = f" for **{matched_role.title}**" if matched_role else ""
        return {
            "reply": (
                f"{student_greeting}I am your Career Planning Assistant{role_mention}. "
                "I can guide you on required technical skills, project ideas, learning sequences, and viva interview preparation. "
                "Feel free to ask questions like:\n"
                "- *What projects should I build for an AI Engineer role?*\n"
                "- *What is the difference between Data Science and MLOps?*\n"
                "- *What core skills should I learn first?*"
            ),
            "is_fallback": True,
            "sources": sources
        }
