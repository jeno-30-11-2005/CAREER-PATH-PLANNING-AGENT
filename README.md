# Intelligent Career Path Planning Agent

**BE Artificial Intelligence & Data Science Mini-Project**  
*An explainable, agentic career guidance platform with deterministic matching, skill-gap analysis, personalized roadmaps, and offline-tolerant AI assistance.*

---

## 🎨 Theme & User Interface
The user interface implements a **Dark Obsidian & Neon Violet Glow** aesthetic:
- **Glassmorphism Panels:** Layered dark cards with subtle borders (`#14141D` on `#0B0B0E`).
- **Accent Glow:** Glowing neon purple and magenta buttons (`#9D4EDD` $\rightarrow$ `#C77DFF`).
- **Interactive Metrics:** "Total Readiness Score", "Skill Inventory", "Curriculum Progress Curve", and "Target Roles Watchlist".
- **Human-in-the-Loop Review:** Dedicated approval modal for agent-proposed curriculum plans before database persistence.

---

## 🚀 Key Modules Built

1. **Module A: Student Academic Profile**
   - Captures education level, degree specialization, year/semester, declared technical & soft skills, experience, and weekly hours.
2. **Module B: Career Role Knowledge Base**
   - 8 pre-seeded industry & academic roles:
     1. Machine Learning Engineer
     2. AI Engineer
     3. Data Analyst
     4. Data Scientist
     5. Backend Developer
     6. Data Engineer
     7. MLOps Engineer
     8. AI Product Engineer
3. **Module C: Deterministic Career Recommendation Engine**
   - Transparent 5-factor weighted algorithm (Skills 40%, Interests 30%, Field Preference 15%, Experience 10%, Goals 5%).
4. **Module D: Skill-Gap Analysis**
   - Categorizes skills into Confirmed (reported), Partially Developed (foundational), and Not Yet Reported, with an educational disclaimer.
5. **Module E & I: Personalized Roadmap & Progress Tracker**
   - 5-phase sequential roadmap (Foundations $\rightarrow$ Core Skills $\rightarrow$ Applied Practice $\rightarrow$ Portfolio Projects $\rightarrow$ Viva Prep).
   - Milestone checkboxes, notes taking, and verified tutorial links.
6. **Module F: Conversational AI Career Assistant**
   - LLM integration using Google Gemini with 100% deterministic offline fallback to the institutional knowledge base.
7. **Module G: Controlled Agentic Workflow**
   - 6-component coordinated pipeline with automated quality guardrails and human review approval.
8. **Module H: Student Dashboard**
   - Executive dashboard tracking progress percentages, readiness curves, and next recommended skills.
9. **Viva & Academic Defense Hub**
   - Built-in viva guide with top 5 examiner questions, answers, and a 10-slide presentation outline.

---

## 🛠️ Technology Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons
- **Backend:** Python 3.11, FastAPI, Pydantic v2, SQLAlchemy ORM, Uvicorn
- **Database:** SQLite (default for instant zero-config setup) / PostgreSQL support
- **Testing:** Pytest (11/11 automated tests passing in 0.70s)
- **AI Integration:** Google Gemini 1.5 Flash + Deterministic Knowledge-Based Fallback

---

## ⚡ How to Run the Project (Windows PowerShell)

### One-Click Launch (Recommended)
Run the master start script in PowerShell:
```powershell
.\scripts\start_all.ps1
```
This opens two terminals:
- **Backend Server:** [http://127.0.0.1:8000](http://127.0.0.1:8000) (Interactive Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs))
- **Frontend App:** [http://localhost:5173](http://localhost:5173)

---

### Manual Launch (Step-by-Step)

#### 1. Start the FastAPI Backend
```powershell
cd "c:\Users\student\Desktop\CAREER PATH PLANNING AGENT"
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Start the React Frontend (in a new PowerShell window)
```powershell
cd "c:\Users\student\Desktop\CAREER PATH PLANNING AGENT\frontend"
$env:PATH = "C:\Users\student\Desktop\CAREER PATH PLANNING AGENT\tools\nodejs;$env:PATH"
npm run dev
```

---

## 🧪 Running Automated Tests

Execute the 11 Pytest verification cases:
```powershell
.\scripts\run_tests.ps1
```
*Expected Result:*
```
11 passed in 0.70s (100% Passing)
```

---

## 📚 Project Documentation
- **[System Architecture](docs/architecture.md):** Complete architecture overview with Mermaid diagrams.
- **[Database Design](docs/database-design.md):** Entity-Relationship (ER) diagram and schema specifications.
- **[Automated Testing Report](docs/testing-report.md):** Detailed breakdown of all 11 test cases and results.
- **[Viva Questions & Answers](docs/viva-questions.md):** Top examiner questions and beginner-friendly answers.
- **[Mini-Project Report Outline](docs/project-report-outline.md):** Chapter-by-chapter college submission template.
- **[Project Journey Log](docs/PROJECT_JOURNEY_LOG.md):** Daily session tracking.
