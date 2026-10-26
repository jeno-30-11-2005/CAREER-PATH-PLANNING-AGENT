# System Architecture: Intelligent Career Path Planning Agent

## 1. Executive Summary & Abstract
The **Intelligent Career Path Planning Agent** is an explainable full-stack decision-support system designed for engineering students in **Artificial Intelligence and Data Science**. It addresses the prevalent dilemma of career uncertainty, misaligned skill preparation, and opaque online career advice.

The system combines:
1. **Deterministic Multi-Factor Scoring**: Transparent mathematical evaluation based on declared skills (40%), interests (30%), field preference (15%), experience level (10%), and goals (5%).
2. **Three-Tier Skill-Gap Matrix**: Distinguishes between confirmed reported skills, partially developed foundational concepts, and unreported competencies.
3. **5-Phase Curriculum Roadmap Generator**: Generates actionable, progressive milestones respecting weekly study hour constraints and verified learning resources.
4. **Controlled Agentic Workflow**: Coordinates 6 distinct analytical components with quality guardrails and human-in-the-loop approval before persistence.
5. **Conversational Career Assistant**: Incorporates Google Gemini with a 100% deterministic knowledge-grounded fallback ensuring resilience in offline evaluations.

---

## 2. Architectural Blueprint

```mermaid
graph TD
    subgraph Client ["Client Presentation Layer (React + TS + Tailwind)"]
        UI_Dash["Executive Dashboard (Obsidian & Neon Glow Theme)"]
        UI_Reco["Career Recommendations View"]
        UI_Gap["Skill-Gap Matrix Visualizer"]
        UI_Roadmap["5-Phase Roadmap Stepper & Notes"]
        UI_Chat["Conversational Career Assistant"]
        UI_Viva["Viva & Academic Defense Hub"]
    end

    subgraph API ["Application Gateway (FastAPI + Pydantic)"]
        Router["FastAPI REST Router (/api/v1)"]
        Validator["Pydantic Runtime Request/Response Sanitizer"]
        CORS["CORS Middleware"]
    end

    subgraph Workflow ["Agentic Orchestration & AI Engine"]
        C1["Component 1: Profile Analysis"]
        C2["Component 2: Deterministic Recommender"]
        C3["Component 3: Skill-Gap Analyzer"]
        C4["Component 4: Roadmap Planning"]
        C5["Component 5: Quality Review & Guardrails"]
        C6["Component 6: Human-in-the-Loop Review"]
        LLM["Google Gemini 1.5 Flash (Configurable)"]
        Fallback["Deterministic Institutional Knowledge Base"]
    end

    subgraph Database ["Data Persistence Layer (SQLAlchemy ORM)"]
        DB_Profiles["student_profiles"]
        DB_Roles["career_roles (8 Roles Seeded)"]
        DB_Roadmaps["learning_roadmaps"]
        DB_Items["roadmap_items"]
        DB_Chats["chat_sessions & messages"]
    end

    Client -->|HTTP / JSON| Router
    Router --> Validator
    Validator --> Workflow
    Workflow --> C1 --> C2 --> C3 --> C4 --> C5 --> C6
    Workflow --> LLM
    LLM -.->|Fallback on Timeout/Offline| Fallback
    Workflow --> Database
```

---

## 3. Technology Stack Justification

| Technology | Role | Justification for College Project |
| :--- | :--- | :--- |
| **Python 3.11** | Backend Language | Dominant language in AI & Data Science; rich ecosystem for statistical analysis and machine learning. |
| **FastAPI** | REST API Framework | Asynchronous performance, automatic OpenAPI/Swagger documentation (`/docs`), seamless Pydantic integration. |
| **Pydantic v2** | Data Validation | Enforces strict type schemas, preventing runtime exceptions and malformed requests. |
| **SQLAlchemy 2.0** | Object-Relational Mapping | Decouples SQL syntax from business logic; facilitates cross-database support (SQLite for local runs, PostgreSQL for production). |
| **React 18 + TypeScript** | Client Frontend | Component reusability, compile-time type safety, robust UI state management. |
| **Tailwind CSS** | Styling System | Utility-first styling enabling the dark obsidian and neon violet glow dashboard aesthetic. |
| **Vite** | Build Tool | Sub-second Hot Module Replacement (HMR) and optimized ES module bundling. |
| **Pytest** | Automated Testing | Comprehensive unit and integration testing covering all 11 core functional modules. |
