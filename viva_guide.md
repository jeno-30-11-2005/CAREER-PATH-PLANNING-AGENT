# College Viva Guide & Project Defense Reference (Enterprise V2.0)

**Project Title:** Intelligent Career Path Planning System  
**Academic Degree:** Bachelor of Engineering (BE) in Artificial Intelligence, Data Science, or Computer Science  
**Architecture:** Database-Driven Full-Stack System (Python, SQLAlchemy, SQLite, Streamlit)  

---

## 1. Project Abstract
The **Intelligent Career Path Planning System** is a comprehensive, database-driven career intelligence platform bridging the gap between student education, technical proficiencies, and industry career opportunities across 50 specialized engineering disciplines.

Unlike static legacy systems with hardcoded dictionaries, the platform employs a normalized relational database (`career_intelligence.db`) with 25 tables, containing **1,511 technical skills** across 90 technology domains, **256 areas of interest**, **505 specialized career profiles**, **459 career progression pathways**, **505 portfolio capstone projects**, and **505 curated learning resources**.

The application features an explainable multi-factor recommendation engine, precise skill-gap analysis, dynamically calibrated 8-stage roadmaps, side-by-side career comparison, ATS-friendly resume parsing (PDF/DOCX), student milestone tracking, and a secure administrative portal.

---

## 2. Key Viva Questions & Concise Model Answers

### Q1: What problem does your project solve?
**Answer:**  
"Engineering and technology students frequently struggle with career indecision, unclear skill requirements, and disorganized study paths. Our platform solves this by providing an explainable, data-backed guidance system that diagnoses a student's current skills and interests, calculates compatibility with 505 specialized industry careers, exposes missing skills with learning timelines, and provides an 8-stage personalized roadmap with step-by-step portfolio projects."

---

### Q2: What is the database architecture of your project?
**Answer:**  
"We designed a normalized relational database in **SQLite** managed through **SQLAlchemy ORM** (`database/models.py`). It consists of 25 structured tables:
- `TechnicalSkill`, `SkillCategory`, `SkillDomain`, `SkillAlias`, `SkillPrerequisite`
- `AreaOfInterest`, `InterestCategory`
- `CareerCategory`, `Career`, `CareerSkill`, `CareerInterest`, `CareerEducation`
- `CareerPathway` (vertical promotions and lateral pivot transitions)
- `Project`, `ProjectSkill`, `ProjectStep`
- `LearningResource`, `CareerResource`
- `StudentProfile`, `StudentSkillInventory`, `StudentRoadmapProgress`, `StudentTargetCareer`
- `AdminUser`, `SystemAuditLog`

Foreign key integrity is strictly enforced with `PRAGMA foreign_keys = ON;`."

---

### Q3: What algorithm or formula is used for career recommendations?
**Answer:**  
"We developed an explainable **Multi-Factor Recommendation Algorithm** (`services/recommendation_service.py`):
$$\text{Skill Score} = (0.70 \times S_{\text{essential}}) + (0.20 \times S_{\text{preferred}}) + (0.10 \times S_{\text{additional}})$$
Where each skill match is weighted by student proficiency (Beginner: 0.50, Intermediate: 0.75, Advanced: 1.00, Expert: 1.15).

The final compatibility score is:
$$\text{Compatibility Score} = (0.65 \times \text{Skill Score}) + (0.25 \times \text{Interest Affinity}) + (0.10 \times \text{Academic Branch Match})$$
This ensures students receive transparent, explainable recommendations without black-box opacity."

---

### Q4: How is Skill Gap Analysis performed?
**Answer:**  
"In `services/skill_gap_service.py`:
1. It compares student skills against the target career's essential, preferred, and additional requirements.
2. It classifies each requirement into **Acquired** (with current proficiency) or **Missing** (with priority levels: Critical, High, Medium).
3. It computes an overall **Readiness Percentage**.
4. It estimates the total study hours required based on skill difficulty and maps it to a completion timeline in weeks according to the student's available weekly study hours."

---

### Q5: How does the 8-Stage Learning Roadmap work?
**Answer:**  
"In `services/roadmap_service.py`, the system organizes missing skills and foundational topics into 8 chronological milestones:
1. Foundational Prerequisites & Environment Setup
2. Core Technical Frameworks & Libraries
3. Data Persistence, APIs & Architecture
4. Advanced Engineering & Production Patterns
5. Testing, Security, Quality & DevOps
6. Hands-on Practical Project Implementation
7. Portfolio Packaging, Documentation & GitHub
8. Placement Preparation, Resume & Mock Interviews

The system dynamically calculates the duration of each stage in weeks based on the student's declared study pace."

---

### Q6: How does the AI Resume Analyzer extract skills?
**Answer:**  
"In `services/resume_service.py`, the system accepts `.pdf`, `.docx`, or `.txt` resumes:
1. It extracts raw text using **PyMuPDF (`fitz`)** for PDFs or **python-docx** for Word documents.
2. It cleans and normalizes the text into token n-grams (unigrams, bigrams, trigrams).
3. It performs regex boundary matching against all 1,511 skill names, canonical aliases, and domain headwords.
4. It calculates the candidate's match rate against any chosen target career and highlights matched vs. missing skills for ATS optimization."

---

### Q7: Why did you redesign the UI into a Single-Page interface inspired by modern dashboards?
**Answer:**  
"Complex systems with 15+ sidebar menus confuse students and examiners. We redesigned the interface into a **Single-Page Progressive Disclosure Experience** inspired by modern minimalist dashboards (CoachPro aesthetic):
1. **Light, Airy Theme:** Soft sage/mint backdrop, deep forest teal accents, rounded white cards, and pastel icon circles.
2. **Step-by-Step Flow:** The student fills in their profile, clicks 'Analyze My Career', sees their top recommended careers, and clicks 'Explore This Career' to immediately reveal the Career Overview, Skill Gap Analysis, 6-Stage Roadmap, Projects, and Resources right below on the same page.
3. **Focused Navigation:** The sidebar contains only 3 primary navigation options (Home, My Career Plan, My Progress) plus quick 1-click profile presets (AI/ML, Web Dev, Cybersecurity) and an optional 'More Tools' section for advanced features."

---

### Q8: How can the system be expanded without changing application code?
**Answer:**  
"Because all career knowledge is decoupled into relational database records, administrators can add new skills, careers, projects, or pathways using the **Admin Management Dashboard** or via bulk CSV/JSON import (`services/admin_service.py`). New records are instantly available in the recommendation engine and explorers without restarting or modifying Python code."

---

## 3. High-Scoring Viva Demonstration Flow
1. **Header & Preset Profiles (`app.py`):** Point out the CoachPro deep teal banner and click 'AI / ML Student' in the sidebar to populate realistic data in 1 second.
2. **Tell Us About Yourself (`ui/single_page_home.py`):** Show the searchable multi-selects for 1,511 technical skills and 256 interest areas, along with proficiency assignment (Beginner, Intermediate, Advanced, Expert).
3. **Run 'Analyze My Career':** Show the top recommended careers (e.g. AI Research Scientist, ML Engineer) with compatibility scores and matching vs missing skill tags.
4. **Click 'Explore This Career':** Show how the details appear right below on the same page:
   - **Career Overview:** Daily responsibilities, education prerequisites, and soft skills.
   - **Skill Gap Analysis:** Readiness score progress bar, possessed skills (green), and missing essential skills (amber) with study timeline.
   - **Personalized 6-Stage Roadmap:** Fundamentals $\rightarrow$ Core Skills $\rightarrow$ Advanced Skills $\rightarrow$ Projects $\rightarrow$ Portfolio $\rightarrow$ Placement Prep, complete with interactive completion checkboxes.
   - **Practical Projects & Verified Resources:** Step-by-step capstones and working documentation links.
   - **Career Progression:** Junior $\rightarrow$ Mid $\rightarrow$ Senior ladder.
5. **My Learning Progress:** Show the live roadmap completion bar and click 'Save Progress to Database'.
6. **More Tools (Optional):** Switch to 'More Tools' to demonstrate the AI Resume Analyzer with PDF/DOCX skill extraction or compare two careers side-by-side.
