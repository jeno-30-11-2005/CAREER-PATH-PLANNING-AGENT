# Intelligent Career Path Planning System — Career Intelligence Platform

**A Simple, Clean, Single-Page Career Intelligence Interface Powered by an Extensive Database**  
Built with **Python**, **SQLAlchemy**, and **Streamlit** (featuring the **CoachPro-inspired Minimalist Light & Sage/Teal Theme**).

---

## 🎯 Project Overview & Vision
The **Career Intelligence Platform** is a streamlined, beginner-friendly career guidance system designed for engineering and technology students. It simplifies the entire career decision workflow into a single, cohesive interface:

$$\text{Student Profile} \longrightarrow \text{Career Recommendations} \longrightarrow \text{Select Career} \longrightarrow \text{Skill Gap Analysis} \longrightarrow \text{Personalized Roadmap} \longrightarrow \text{Projects \& Resources} \longrightarrow \text{Track Progress}$$

### ✨ Key Design Principles:
1. **Single-Page Simplicity:** No 15-menu sidebar overload. Everything a student needs unfolds step-by-step on one clean page.
2. **CoachPro Aesthetic:** Soft, airy light palette with sage/mint backdrop, deep forest teal accents, rounded white cards, and pastel icon circles.
3. **Extensive Relational Database:** Full SQLite relational database (`career_intelligence.db`) with 25 tables, 1,511 skills, 505 careers, 256 interests, 505 projects, 505 resources, and 459 pathways.
4. **Beginner-Friendly:** Clear typography, easy inputs, and plain-English explanations.

---

## 📊 Database Metrics & Coverage Summary
The relational database (`career_intelligence.db`) is fully normalized across 25 tables using SQLAlchemy ORM:

| Metric Category | Target | Actual Database Count | Verification Status |
| :--- | :---: | :---: | :---: |
| **Technical Skills** | 1,500+ | **1,511** (across 90 domains) | ✅ 100% Verified |
| **Areas of Interest** | 250+ | **256** (across 27 categories) | ✅ 100% Verified |
| **Career Families** | 50 | **50** (comprehensive domains) | ✅ 100% Verified |
| **Specialized Careers** | 500+ | **505** (detailed role profiles) | ✅ 100% Verified |
| **Career-Skill Mappings** | 1,000+ | **2,609** (70% Essential, 20% Preferred, 10% Additional) | ✅ 100% Verified |
| **Career Pathways** | 200+ | **459** (Vertical & Lateral progressions) | ✅ 100% Verified |
| **Portfolio Projects** | 500+ | **505** (With step-by-step deliverables) | ✅ 100% Verified |
| **Learning Resources** | 500+ | **505** (Verified documentation & courses) | ✅ 100% Verified |

---

## 🧭 Single-Page Guided Workflow

The application interface is structured into one progressive workflow:

1. **Header & Profile Overview:**
   - Deep forest teal gradient welcome banner with student profile badge.
   - 4 quick metric cards with pastel circular icons (Skills Declared, Interest Areas, Weekly Pace, Milestones Completed).
2. **1. Tell Us About Yourself:**
   - Basic details: Name, Education Level, Academic Branch, Semester.
   - Searchable multi-select for technical skills (from 1,511 options) with proficiency adjustments (Beginner, Intermediate, Advanced, Expert).
   - Custom skill input for new/unlisted skills.
   - Searchable multi-select for areas of interest (from 256 options) and optional career goal.
   - Big action button: **"Analyze My Career"**.
3. **2. Your Recommended Careers:**
   - Top 5-10 recommended career cards with compatibility scores (0–100%).
   - Displays matched skills, key skills to learn, and natural language explanation.
   - One-click action: **"Explore This Career"**.
4. **3. Career Intelligence Details (Appears on the SAME PAGE):**
   - **📋 Career Overview:** What it is, daily responsibilities, degree requirements, soft skills.
   - **📊 Skill Gap Analysis:** Readiness score bar, acquired skills, and missing essential skills with priority tags.
   - **🗺️ Personalized 6-Stage Roadmap:** Fundamentals $\rightarrow$ Core Skills $\rightarrow$ Advanced Skills $\rightarrow$ Practical Projects $\rightarrow$ Portfolio Building $\rightarrow$ Interview Preparation with completion checkboxes.
   - **📁 Practical Projects:** Capstones tailored to the career with tools, deliverables, and difficulty.
   - **📚 Learning Resources:** Verified documentation and free/paid courses with direct links.
   - **🪜 Career Progression:** Junior $\rightarrow$ Mid $\rightarrow$ Senior ladder with transition milestones.
5. **4. My Learning Progress:**
   - Real-time roadmap progress bar and database persistence button.
6. **Simple Minimal Sidebar Navigation:**
   - **🏠 Home:** Complete single-page experience.
   - **📋 My Career Plan:** Focused view of the selected career and roadmap.
   - **📈 My Progress:** Learning milestones and skills inventory.
   - **🧰 More Tools:** Optional access to the AI Resume Analyzer, Career Comparison Tool, and Admin Portal.
   - **💡 Quick Profile Presets:** 1-click loaders for AI/ML, Web Dev, or Cybersecurity students.

---

## ⚡ How to Run the Application Manually (Windows)

### Method 1: One-Click Launch (Easiest)
In your Windows File Explorer, navigate to:
`c:\Users\Ashlin jeno m\OneDrive\Desktop\CAREER-PATH-PLANNING-AGENT-main`
Double-click:
```cmd
run_app.bat
```

### Method 2: Windows PowerShell
```powershell
cd "c:\Users\Ashlin jeno m\OneDrive\Desktop\CAREER-PATH-PLANNING-AGENT-main"
.\venv\Scripts\python.exe -m streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 🧪 Automated Verification Suite
To verify all 10 system components, database targets, scoring calculations, and resume extraction:

### Method 1: One-Click Batch Script
Double-click:
```cmd
run_tests.bat
```

### Method 2: Windows PowerShell
```powershell
.\venv\Scripts\python.exe test_system.py
```
*Expected Result: `[SUCCESS] ALL 10 END-TO-END VERIFICATION TESTS PASSED WITH 100% SUCCESS!`*
