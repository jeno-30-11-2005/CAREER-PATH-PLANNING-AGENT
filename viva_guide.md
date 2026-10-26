# College Viva Guide & Project Report Outline

**Project Title:** Intelligent Career Path Planning System  
**Academic Degree:** Bachelor of Engineering (BE) in Artificial Intelligence and Data Science  
**Student Level:** Beginner / Mini-Project  

---

## 1. Project Overview & Abstract
The **Intelligent Career Path Planning System** is a lightweight, rule-based web application developed in **Python and Streamlit**. It solves the problem of student career indecision by taking a student's academic background, skills, and interests, evaluating their compatibility against 4 core career tracks (**AI Engineer, ML Engineer, Data Analyst, and Python Developer**), highlighting missing skills in an explainable skill-gap matrix, and presenting a structured 4-phase learning roadmap.

---

## 2. Top 6 Viva Questions & Beginner-Friendly Answers

### Q1: What is the main objective of your mini-project?
**Answer:**  
"The main objective is to provide students with an explainable career guidance tool that:
1. Collects student academic details, skills, and interests.
2. Calculates compatibility scores for target careers.
3. Identifies skill gaps by separating skills already possessed from skills that need to be learned.
4. Generates a step-by-step 4-phase learning roadmap with timelines and milestones."

---

### Q2: What algorithm or formula did you use for career recommendations?
**Answer:**  
"We use a transparent **Weighted Rule-Based Scoring Formula**:
$$\text{Match Score} = (\text{Skill Match Ratio} \times 0.70) + (\text{Interest Match Ratio} \times 0.30) \times 100$$
- **Skill Match Ratio:** Number of skills the student has that match the role, divided by total skills required. Weighted at **70%** because technical proficiency is fundamental.
- **Interest Match Ratio:** Overlap of student interests with the domain, weighted at **30%**."

---

### Q3: Why did you choose Streamlit instead of a complex frontend and backend?
**Answer:**  
"Streamlit allows writing both user interface and application logic in pure Python without needing HTML, CSS, JavaScript, or separate REST API servers. This keeps the codebase small, eliminates external connection errors, makes the project easy to debug, and allows me to explain every line of code during my viva."

---

### Q4: How is the Skill-Gap Analysis calculated in your code?
**Answer:**  
"In `logic.py`, the `analyze_skill_gap()` function converts the student's declared skills into a Python set and iterates over the target career's required skills.
- If a required skill exists in the student's set, it is added to `acquired` (Green column).
- If it does not exist, it is added to `missing` (Needs to learn column).
- It also computes a readiness percentage: $\frac{\text{len(acquired)}}{\text{len(required)}} \times 100$."

---

### Q5: What Python data structures did you use in your project?
**Answer:**  
"We used three fundamental Python data structures:
1. **Dictionaries (`dict`):** Used in `career_data.py` to store key-value information for each career (title, description, required skills, and roadmap).
2. **Lists (`list`):** Used to store sequential roadmap steps and selectable options.
3. **Sets (`set`):** Used in `logic.py` for efficient $O(1)$ membership lookup when comparing student skills against required career skills."

---

### Q6: What are the 4 progressive steps in your Career Roadmap?
**Answer:**  
"Every career track contains a 4-phase progressive roadmap:
1. **Step 1: Foundations (Weeks 1-3):** Basic programming, syntax, and tools like Git.
2. **Step 2: Core Concepts (Weeks 4-6):** Specialized domain libraries (e.g. Pandas, Scikit-Learn, Prompt Engineering).
3. **Step 3: Practical Projects (Weeks 7-9):** Hands-on application building (e.g. Predictor models or APIs).
4. **Step 4: Portfolio & Viva (Weeks 10-12):** Documentation, GitHub repositories, and presentation practice."

---

## 3. Sample Student Scenarios for Viva Demonstration

| Scenario | Inputs | Expected Output |
| :--- | :--- | :--- |
| **Profile A (AI Focus)** | Skills: Python, Prompt Engineering, FastAPI<br>Interests: Artificial Intelligence, Generative AI | **#1 Match: AI Engineer** (~47% - 85% match)<br>Skill Gap: Needs Deep Learning Basics, Vector Databases. |
| **Profile B (Data Analytics)** | Skills: SQL, Excel / Spreadsheets<br>Interests: Data Visualization, Business Analytics | **#1 Match: Data Analyst**<br>Skill Gap: Needs PowerBI / Tableau, Python (Pandas). |
| **Profile C (Beginner)** | Skills: (None selected)<br>Interests: Machine Learning | **#1 Match: ML Engineer** (25% interest baseline)<br>Skill Gap: Clearly displays all required skills in Step 1. |

---

## 4. Mini-Project Report Outline

- **Chapter 1: Introduction**
  - 1.1 Motivation & Background
  - 1.2 Problem Statement
  - 1.3 Project Objectives
- **Chapter 2: System Analysis & Design**
  - 2.1 Functional Requirements (Student Details, Recommendations, Skill Gap, Roadmap)
  - 2.2 System Architecture Diagram
  - 2.3 Data Dictionary (`career_data.py`)
- **Chapter 3: Methodology & Implementation**
  - 3.1 Scoring Algorithm Formulation
  - 3.2 Skill-Gap Classification Logic
  - 3.3 Streamlit Interactive Interface (`app.py`)
- **Chapter 4: Testing & Results**
  - 4.1 Automated Test Execution (`test_system.py`)
  - 4.2 Test Scenarios & Verification Evidence
- **Chapter 5: Conclusion & Future Scope**
  - 5.1 Project Summary
  - 5.2 Future Enhancements (Adding more career roles, resume parsing)
