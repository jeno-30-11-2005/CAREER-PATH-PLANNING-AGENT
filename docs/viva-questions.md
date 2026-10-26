# Beginner-Friendly Viva Questions & Answers

### Q1: What is the Intelligent Career Path Planning Agent and what problem does it solve?
**Answer:**  
The Intelligent Career Path Planning Agent is a full-stack educational decision-support platform for engineering students (specifically in AI & Data Science). Many students struggle with career direction, do not know which skills match their interests, lack awareness of their skill gaps, and get overwhelmed by unverified internet advice. Our system provides personalized, explainable career role recommendations, analyzes skill gaps, builds structured 5-phase learning roadmaps, and provides an AI career assistant with an offline fallback.

---

### Q2: How does your system differ from a student asking ChatGPT directly?
**Answer:**  
Direct prompting with ChatGPT suffers from three severe limitations:
1. **Hallucination:** An LLM might invent unrealistic timelines, recommend random courses, or make exaggerated hiring promises.
2. **Lack of Persistence:** Ordinary chat sessions do not track completed milestones or calculate true progress over time.
3. **No Quality Verification:** ChatGPT does not validate whether prerequisites are satisfied.

In our project, we use an **Orchestrated Agentic Workflow** with 6 coordinated stages:
1. Profile Analysis $\rightarrow$
2. Deterministic Recommendation Algorithm $\rightarrow$
3. Skill-Gap Categorization $\rightarrow$
4. Roadmap Planning with prerequisite sequencing $\rightarrow$
5. Quality Review Guardrails $\rightarrow$
6. Human-in-the-Loop Review before committing changes to the database.

---

### Q3: How is the Recommendation Score calculated?
**Answer:**  
The score is calculated deterministically using a multi-factor weighted formula:
- **Technical Skills Match (40%):** Compares declared skills with required and recommended role skills.
- **Interest Match (30%):** Measures overlap between student interests and the role domain.
- **Preferred Career Field Match (15%):** Checks if the student's field preference matches the role category.
- **Experience Level (10%):** Evaluates beginner, intermediate, or advanced compatibility.
- **Career Goals (5%):** Analyzes alignment with personal aspirations.

Scores are normalized between 15% and 98.5% and presented strictly as educational compatibility, never as employment guarantees.

---

### Q4: Explain the 5 phases of your generated Learning Roadmap.
**Answer:**  
Every career roadmap is structured into 5 progressive pedagogical phases:
1. **Foundations:** Prerequisite math, logic, and fundamental computer science concepts.
2. **Core Technical Skills:** Core libraries and frameworks directly demanded for the role (e.g. Scikit-Learn for ML, FastAPI for Backend).
3. **Applied Practice:** Developer tooling, environment configuration, and pipeline integration.
4. **Portfolio Projects:** Capstone projects with GitHub repositories and documentation suitable for college recruitment.
5. **Interview Preparation:** Technical questions, algorithmic trade-offs, and project defense preparation.

---

### Q5: What is the role of Pydantic in your project?
**Answer:**  
Pydantic is a data validation library for Python. In our FastAPI backend, Pydantic schemas validate all incoming HTTP requests and format outgoing responses. If a user submits invalid data (e.g. negative study hours or missing fields), Pydantic catches it immediately and returns an HTTP 422 error, protecting the application and database from corrupted data.

---

### Q6: How does the system handle an offline situation or LLM API failure?
**Answer:**  
Our system includes a **Deterministic Rule-Based Fallback Engine**. If Google Gemini is unavailable or no API key is provided, the assistant does not crash. Instead, it queries our verified institutional Career Knowledge Base to answer inquiries about required skills, project ideas, learning sequences, and interview preparation.
