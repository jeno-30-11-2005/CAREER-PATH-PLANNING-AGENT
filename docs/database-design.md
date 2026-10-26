# Database Design & Entity-Relationship (ER) Documentation

## 1. Database Architecture Overview
The system uses a normalized relational database design managed through **SQLAlchemy ORM**. It operates on **SQLite** for rapid, zero-setup local development and directly connects to **PostgreSQL** in production by updating `DATABASE_URL` in `.env`.

---

## 2. Entity-Relationship Diagram

```mermaid
erDiagram
    STUDENT_PROFILES ||--o{ CAREER_RECOMMENDATIONS : receives
    STUDENT_PROFILES ||--o{ LEARNING_ROADMAPS : owns
    STUDENT_PROFILES ||--o{ CHAT_SESSIONS : conducts
    CAREER_ROLES ||--o{ CAREER_RECOMMENDATIONS : targets
    CAREER_ROLES ||--o{ LEARNING_ROADMAPS : blueprints
    LEARNING_ROADMAPS ||--|{ ROADMAP_ITEMS : contains
    CHAT_SESSIONS ||--|{ CHAT_MESSAGES : contains

    STUDENT_PROFILES {
        int id PK
        string name
        string education_level
        string degree_specialization
        string current_year_sem
        json interests
        json technical_skills
        json soft_skills
        string programming_experience
        json preferred_career_fields
        int weekly_learning_hours
        text career_goals
        datetime created_at
        datetime updated_at
    }

    CAREER_ROLES {
        int id PK
        string slug UK
        string title
        string category
        text description
        json required_skills
        json recommended_skills
        json tools_technologies
        json example_projects
        json learning_sequence
        json prerequisites
        datetime created_at
    }

    CAREER_RECOMMENDATIONS {
        int id PK
        int student_profile_id FK
        int career_role_id FK
        float match_score
        json matching_interests
        json matching_skills
        json missing_skills
        text explanation
        json suggested_next_steps
        datetime created_at
    }

    LEARNING_ROADMAPS {
        int id PK
        int student_profile_id FK
        int career_role_id FK
        string title
        string target_role
        int weekly_hours
        int total_estimated_weeks
        bool is_approved
        string generation_method
        datetime created_at
        datetime updated_at
    }

    ROADMAP_ITEMS {
        int id PK
        int roadmap_id FK
        string phase
        int step_number
        string skill_topic
        text why_it_matters
        json prerequisites
        text suggested_activity
        int estimated_effort_hours
        text practical_exercise
        text milestone_project
        string completion_status
        json resource_links
        text learning_notes
    }

    CHAT_SESSIONS {
        int id PK
        int student_profile_id FK
        string title
        string selected_role_slug
        datetime created_at
    }

    CHAT_MESSAGES {
        int id PK
        int session_id FK
        string role
        text content
        bool is_fallback
        datetime timestamp
    }
```

---

## 3. Seeded Career Roles

The database is initialized with 8 complete career profiles:
1. **Machine Learning Engineer** (`ml-engineer`)
2. **AI Engineer** (`ai-engineer`)
3. **Data Analyst** (`data-analyst`)
4. **Data Scientist** (`data-scientist`)
5. **Backend Developer** (`backend-developer`)
6. **Data Engineer** (`data-engineer`)
7. **MLOps Engineer** (`mlops-engineer`)
8. **AI Product Engineer** (`ai-product-engineer`)
