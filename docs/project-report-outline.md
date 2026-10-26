# BE Mini-Project Report Outline: Intelligent Career Path Planning Agent

**Department:** Artificial Intelligence and Data Science  
**Degree:** Bachelor of Engineering (BE)  

---

## Chapter 1: Introduction
- 1.1 Project Overview & Motivation
- 1.2 Problem Statement & Industry Context
- 1.3 Limitations of Existing Career Advising Systems
- 1.4 Objectives & Scope of the Proposed Agent
- 1.5 Organization of the Report

## Chapter 2: Literature Survey & Background Study
- 2.1 Evolution of Career Guidance Platforms
- 2.2 Rule-Based Systems vs. Machine Learning in Education
- 2.3 Large Language Models (LLMs) & Agentic Workflows
- 2.4 Ethical AI and Guardrails in Educational Recommendation

## Chapter 3: System Requirements & Architecture
- 3.1 Functional Requirements (FR)
  - Student Profile Management
  - Deterministic Career Role Recommendation
  - Skill-Gap Matrix Categorization
  - Multi-Phase Roadmap Generation & Progress Tracking
  - AI Assistant with Offline Resilience
- 3.2 Non-Functional Requirements (NFR)
  - Response latency (< 500ms for API endpoints)
  - Strict input validation via Pydantic
  - High availability and offline tolerance
- 3.3 System Architecture (Three-Tier Client-Server Architecture)
- 3.4 Data Flow Diagrams (Level 0 & Level 1)

## Chapter 4: Database Modeling & Design
- 4.1 Schema Normalization & Entity Definition
- 4.2 Entity-Relationship (ER) Diagram
- 4.3 Seed Knowledge Base (8 Industry Roles)
- 4.4 Data Migration & ORM Mapping with SQLAlchemy

## Chapter 5: Methodology & Implementation
- 5.1 Multi-Factor Weighted Scoring Algorithm (Mathematical Formulation)
- 5.2 Skill-Gap Categorization Logic (Confirmed, Partial, Unreported)
- 5.3 5-Phase Curriculum Roadmap Construction
- 5.4 Agentic Workflow Orchestration (6 Coordinated Components)
- 5.5 Frontend Design (Obsidian & Neon Glow Aesthetic with React + Vite + Tailwind)
- 5.6 Conversational Assistant & Offline Fallback Engine

## Chapter 6: Testing, Results & Discussion
- 6.1 Pytest Automated Testing Methodology
- 6.2 Test Cases & Execution Results (11/11 Verified Cases)
- 6.3 Performance Benchmarks & Response Times
- 6.4 User Interface Walkthrough & Screenshots

## Chapter 7: Conclusion & Future Scope
- 7.1 Summary of Contributions
- 7.2 System Limitations
- 7.3 Future Enhancements (RAG over university syllabus, resume parsing, live job market scraping)
- 7.4 Concluding Remarks

## References
1. FastAPI Documentation: https://fastapi.tiangolo.com/
2. SQLAlchemy 2.0 Unified Documentation: https://docs.sqlalchemy.org/
3. React 18 & Vite Architecture: https://react.dev/
4. Google Gemini Developer Guide: https://ai.google.dev/
