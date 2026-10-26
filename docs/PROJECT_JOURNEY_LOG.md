# Project Journey Log: Intelligent Career Path Planning Agent

**Student Name / Developer:** BE Artificial Intelligence and Data Science Student  
**Project Title:** Intelligent Career Path Planning Agent  
**Academic Year:** 2026-2027  

---

## Session 1: Full-Stack Implementation, Architecture, Testing & Documentation

- **Date:** Today
- **Goal:** Build the complete end-to-end Intelligent Career Path Planning Agent matching all specification modules (A-J), applying the requested Dark Obsidian & Neon Violet glow UI theme, creating the 11-case automated test suite, and preparing college viva documentation.
- **Concepts Learned & Demonstrated:**
  - *Full-Stack Decoupled Architecture:* React + TypeScript + Vite + Tailwind CSS frontend communicating via REST with a Python FastAPI + Pydantic backend.
  - *Deterministic Recommendation Scoring:* 5-factor weighted algorithm (Skills 40%, Interests 30%, Field Preference 15%, Experience 10%, Goals 5%) that operates transparently and offline.
  - *Three-Tier Skill-Gap Categorization:* Confirmed (self-reported), Partially Developed (foundations present), and Not Yet Reported competencies with prioritized learning orders.
  - *5-Phase Curriculum Roadmaps:* Foundations $\rightarrow$ Core Technical $\rightarrow$ Applied Practice $\rightarrow$ Portfolio Projects $\rightarrow$ Viva Preparation, tailored to weekly study hour constraints.
  - *Agentic AI Orchestrator:* Coordinated 6-component pipeline (Profile Analysis, Recommender, Gap Analyzer, Roadmap Planner, Quality Review Guardrail, and Human-in-the-Loop review).
  - *Graceful LLM Fallback:* Gemini 1.5 Flash integration with 100% deterministic knowledge base fallback when offline.
  - *Testing with Pytest:* 11/11 automated tests covering validation, database ORM, recommendation math, skill gaps, roadmaps, dashboard metrics, and agentic workflows.
- **Files Created / Modified:**
  - `backend/app/main.py`: FastAPI server entrypoint with CORS and DB auto-seed.
  - `backend/app/core/config.py`: Environment configuration via Pydantic Settings.
  - `backend/app/db/session.py` & `init_db.py`: SQLAlchemy session and automatic seed script.
  - `backend/app/db/seed_data.py`: Knowledge base containing 8 complete AI/DS roles.
  - `backend/app/models/entities.py`: Relational models (Profiles, Roles, Recommendations, Roadmaps, Items, Progress, Chats).
  - `backend/app/schemas/career_schemas.py`: Pydantic validation schemas.
  - `backend/app/services/`: Career service, recommendation engine, skill-gap service, roadmap service, AI assistant service.
  - `backend/app/agents/workflow.py`: 6-component agentic planning workflow.
  - `backend/app/api/v1/endpoints/`: Health, Profiles, Careers, Recommendations, Skill Gap, Roadmaps, Assistant, Dashboard, Workflow routes.
  - `backend/tests/test_career_agent.py`: 11-case Pytest test suite.
  - `frontend/src/`: React 18 + TypeScript + Tailwind UI matching reference dark obsidian & violet glow dashboard theme.
  - `frontend/src/components/`: Sidebar, Header, ProfileModal, WorkflowModal.
  - `frontend/src/pages/`: DashboardView, RecommendationsView, SkillGapView, RoadmapView, AssistantView, VivaPrepView.
  - `docs/`: architecture.md, database-design.md, testing-report.md, viva-questions.md, project-report-outline.md.
  - `scripts/`: start_backend.ps1, start_frontend.ps1, start_all.ps1, run_tests.ps1.
- **Tests Executed & Actual Results:**
  - 11/11 tests executed via Pytest in 0.70 seconds. **Status: 100% PASSED.**
  - Frontend production build compiled via `tsc && vite build` in 1.71s with zero errors.
- **Current Completion Status:** 100% Complete & Verified.
- **Viva Revision Questions Mastered:**
  1. *What is an Agentic Workflow and how is it different from a simple prompt?*
  2. *How is the Recommendation Score calculated mathematically?*
  3. *Why do we use FastAPI and Pydantic for validation?*
  4. *How does the system ensure reliability if the LLM or internet is down?*
