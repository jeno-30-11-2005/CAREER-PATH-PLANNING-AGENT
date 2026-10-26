from typing import List, Dict, Any

CAREER_ROLES_SEED: List[Dict[str, Any]] = [
    {
        "slug": "ml-engineer",
        "title": "Machine Learning Engineer",
        "category": "Artificial Intelligence & Data Science",
        "description": "Designs, builds, and deploys predictive machine learning models into production systems, bridging data science algorithms with software engineering.",
        "required_skills": [
            "Python",
            "Linear Algebra & Statistics",
            "Scikit-Learn",
            "Data Preprocessing & Feature Engineering",
            "Model Evaluation Metrics",
            "Git & Version Control"
        ],
        "recommended_skills": [
            "Deep Learning (PyTorch/TensorFlow)",
            "Docker",
            "FastAPI / Model Serving",
            "SQL & Relational Databases",
            "MLflow / Experiment Tracking"
        ],
        "tools_technologies": [
            "Python", "NumPy", "Pandas", "Scikit-Learn", "PyTorch", "FastAPI", "Docker", "MLflow", "Git"
        ],
        "example_projects": [
            "Customer Churn Prediction API with Scikit-Learn & FastAPI",
            "End-to-End Housing Price Regressor with Pipeline Deployment",
            "Credit Card Fraud Detection using Imbalanced Learning Techniques"
        ],
        "learning_sequence": [
            "1. Advanced Python & Vectorized Math (NumPy/Pandas)",
            "2. Classical ML Algorithms & Statistical Modeling",
            "3. Deep Learning Fundamentals & Architectures",
            "4. Production Model Packaging (REST APIs & Docker)",
            "5. Monitoring & Continuous Evaluation"
        ],
        "prerequisites": ["Basic Python Syntax", "High School Mathematics & Calculus"]
    },
    {
        "slug": "ai-engineer",
        "title": "AI Engineer",
        "category": "Artificial Intelligence & Data Science",
        "description": "Specializes in developing modern AI applications utilizing foundation models, Large Language Models (LLMs), RAG architectures, and autonomous agent frameworks.",
        "required_skills": [
            "Python",
            "LLM APIs & Prompt Engineering",
            "Vector Databases & Embeddings",
            "Retrieval-Augmented Generation (RAG)",
            "FastAPI / Backend Integration",
            "API Authentication & Security"
        ],
        "recommended_skills": [
            "LangChain / LlamaIndex",
            "Agentic Workflow Orchestration",
            "Fine-Tuning Techniques (LoRA/PEFT)",
            "Evaluation Metrics for LLMs (ROUGE/BLEU/RAGAS)",
            "Docker & Containerization"
        ],
        "tools_technologies": [
            "Python", "OpenAI / Gemini SDK", "LangChain", "ChromaDB / Qdrant", "FastAPI", "Hugging Face", "Docker"
        ],
        "example_projects": [
            "Domain-Specific Knowledge Base RAG Assistant with Source Citations",
            "Multi-Agent Code Review & Debugging Pipeline",
            "Automated Customer Support Agent with Tool Calling"
        ],
        "learning_sequence": [
            "1. Modern Python Async Programming & REST APIs",
            "2. Foundation Models, Prompting & Tokenization",
            "3. Embeddings, Semantic Search & Vector DBs",
            "4. Retrieval-Augmented Generation (RAG) Architecture",
            "5. Agentic Systems, Tool Use & Guardrails"
        ],
        "prerequisites": ["Intermediate Python", "Familiarity with Web APIs"]
    },
    {
        "slug": "data-analyst",
        "title": "Data Analyst",
        "category": "Data & Analytics",
        "description": "Transforms raw business and experimental data into actionable insights, dashboards, and executive reports to drive evidence-based decisions.",
        "required_skills": [
            "Advanced SQL (Joins, Window Functions)",
            "Data Visualization (PowerBI / Tableau)",
            "Exploratory Data Analysis (EDA)",
            "Python or R for Analytics",
            "Descriptive & Inferential Statistics",
            "Business Communication"
        ],
        "recommended_skills": [
            "Pandas & Seaborn",
            "Excel Advanced (VLOOKUP, Pivot Tables)",
            "A/B Testing & Hypothesis Testing",
            "Storytelling with Data"
        ],
        "tools_technologies": [
            "SQL (PostgreSQL/MySQL)", "Python", "Pandas", "PowerBI", "Tableau", "Excel", "Jupyter Notebooks"
        ],
        "example_projects": [
            "E-Commerce Sales Performance & Cohort Retention Dashboard",
            "Healthcare Patient Wait Time Analysis with Statistical Hypothesis Testing",
            "Customer Segmentation Analysis using RFM Methodology"
        ],
        "learning_sequence": [
            "1. Advanced SQL Querying & Database Schema Understanding",
            "2. Business Statistics & Hypothesis Testing",
            "3. Data Cleaning & Wrangling with Pandas",
            "4. Interactive BI Dashboard Design",
            "5. Executive Reporting & Presentation"
        ],
        "prerequisites": ["Basic Computer Literacy", "Elementary Mathematics"]
    },
    {
        "slug": "data-scientist",
        "title": "Data Scientist",
        "category": "Data & Analytics",
        "description": "Combines advanced mathematics, statistical modeling, machine learning, and domain expertise to solve complex predictive and exploratory questions.",
        "required_skills": [
            "Python or R",
            "Probability & Mathematical Statistics",
            "Machine Learning Algorithms",
            "Exploratory Data Analysis & Feature Engineering",
            "SQL & Relational Databases",
            "A/B Testing & Causal Inference"
        ],
        "recommended_skills": [
            "Data Storytelling & Executive Presentations",
            "Big Data Basics (Spark/PySpark)",
            "Time Series Forecasting (ARIMA/Prophet)",
            "Cloud Data Warehouses (BigQuery/Snowflake)"
        ],
        "tools_technologies": [
            "Python", "Jupyter", "Pandas", "Scikit-Learn", "Statsmodels", "SQL", "Matplotlib", "Seaborn"
        ],
        "example_projects": [
            "Predictive Hospital Readmission Classifier with Interpretability (SHAP)",
            "Retail Demand & Inventory Time-Series Forecasting Engine",
            "A/B Test Design and Analysis for User Onboarding Conversion"
        ],
        "learning_sequence": [
            "1. Rigorous Applied Statistics & Probability",
            "2. Deep Python Data Analysis (Pandas, SciPy, Statsmodels)",
            "3. Supervised & Unsupervised Machine Learning",
            "4. Experimental Design & Causal Inference",
            "5. Model Interpretability & Business Case Synthesis"
        ],
        "prerequisites": ["Calculus & Linear Algebra", "Intermediate Python"]
    },
    {
        "slug": "backend-developer",
        "title": "Backend Developer",
        "category": "Software Engineering",
        "description": "Architects, builds, tests, and maintains scalable server-side systems, REST/GraphQL APIs, database persistence layers, and application security.",
        "required_skills": [
            "Python (FastAPI / Django) or Node.js / Java",
            "Relational Database Design & SQL",
            "RESTful API Design & HTTP Standards",
            "Data Validation & ORM (SQLAlchemy / Pydantic)",
            "Authentication & Authorization (JWT, OAuth2)",
            "Git & Version Control"
        ],
        "recommended_skills": [
            "Docker & Containerization",
            "Caching (Redis)",
            "Automated Testing (Pytest)",
            "CI/CD Pipelines (GitHub Actions)",
            "Message Brokers (RabbitMQ / Kafka)"
        ],
        "tools_technologies": [
            "FastAPI", "Python", "PostgreSQL", "SQLAlchemy", "Redis", "Docker", "Git", "Pytest", "Postman"
        ],
        "example_projects": [
            "Secure E-Commerce REST API with Stripe Webhooks & JWT Auth",
            "Real-Time Chat & Notification Server with WebSockets",
            "Role-Based Access Control (RBAC) System with Database Migrations"
        ],
        "learning_sequence": [
            "1. Core Programming & Object-Oriented Design",
            "2. Relational Database Modeling & ACID Transactions",
            "3. REST API Engineering with FastAPI/Pydantic",
            "4. Security, Auth & Token Management",
            "5. Containerization, Testing & Deployment"
        ],
        "prerequisites": ["Basic Programming Syntax", "Understanding of Client-Server Concept"]
    },
    {
        "slug": "data-engineer",
        "title": "Data Engineer",
        "category": "Data Infrastructure",
        "description": "Constructs robust, automated pipelines to extract, transform, clean, and load large-scale data into operational warehouses and data lakes.",
        "required_skills": [
            "Advanced SQL & Schema Optimization",
            "Python for ETL / ELT Pipeline Automation",
            "Data Warehousing Concepts (Star/Snowflake Schema)",
            "Distributed Computing Basics (PySpark)",
            "Workflow Orchestration (Apache Airflow / Dagster)",
            "Linux & Bash Scripting"
        ],
        "recommended_skills": [
            "Cloud Storage & Data Warehouses (AWS S3, BigQuery, Snowflake)",
            "Streaming Data (Kafka)",
            "Data Quality Frameworks (Great Expectations)",
            "Docker"
        ],
        "tools_technologies": [
            "Python", "PostgreSQL", "Apache Airflow", "PySpark", "dbt", "Docker", "Linux/Bash"
        ],
        "example_projects": [
            "Automated Daily Weather & Traffic ETL Pipeline with Airflow and Postgres",
            "E-Commerce Analytics Warehouse Modeling with dbt and Snowflake/Postgres",
            "Streaming Event Logger and Aggregator using PySpark"
        ],
        "learning_sequence": [
            "1. Advanced SQL & Relational Normalization / Denormalization",
            "2. Python Data Extraction (APIs, Scraping, File Processing)",
            "3. Data Warehouse Design (Kimball Dimensional Modeling)",
            "4. Pipeline Orchestration with Airflow / Cron",
            "5. Distributed Processing & Big Data Foundations"
        ],
        "prerequisites": ["Intermediate Python", "Relational Database Fundamentals"]
    },
    {
        "slug": "mlops-engineer",
        "title": "MLOps Engineer",
        "category": "AI Infrastructure & Operations",
        "description": "Automates the lifecycle of machine learning models from CI/CD, deployment, and containerization to automated retraining and drift monitoring.",
        "required_skills": [
            "Docker & Containerization",
            "CI/CD Pipelines (GitHub Actions / GitLab CI)",
            "Python & Shell Scripting",
            "Model Registry & Experiment Tracking (MLflow)",
            "Model Serving Frameworks (FastAPI / Triton)",
            "Linux Systems Administration"
        ],
        "recommended_skills": [
            "Kubernetes & Orchestration (K8s / KServe)",
            "Data & Model Versioning (DVC)",
            "Data Drift Monitoring (Evidently AI / Prometheus)",
            "Infrastructure as Code (Terraform)"
        ],
        "tools_technologies": [
            "Docker", "Kubernetes", "MLflow", "GitHub Actions", "FastAPI", "DVC", "Linux", "Prometheus"
        ],
        "example_projects": [
            "Automated Model Training and Deployment Pipeline with GitHub Actions & Docker",
            "Production ML Model Monitoring Dashboard with Evidently AI and FastAPI",
            "DVC-Tracked Machine Learning Experiment Workflow with Remote Storage"
        ],
        "learning_sequence": [
            "1. Linux Server Management & Docker Fundamentals",
            "2. CI/CD Pipeline Automation for Python Projects",
            "3. Model Packaging, Versioning & Artifact Registries (MLflow)",
            "4. Automated Testing & Continuous Deployment",
            "5. Production Monitoring, Alerting & Model Drift"
        ],
        "prerequisites": ["Machine Learning Basics", "Intermediate Python & Git"]
    },
    {
        "slug": "ai-product-engineer",
        "title": "AI Product Engineer",
        "category": "Product & Applied AI",
        "description": "Bridges user-facing application development with state-of-the-art AI capabilities, crafting intuitive UI/UX for generative AI and autonomous workflows.",
        "required_skills": [
            "Full-Stack Web Development (React / Next.js & TypeScript)",
            "Python / Node.js Backend APIs",
            "LLM Integration & Streaming Responses (SSE / WebSockets)",
            "UI/UX for Generative Interfaces & Human-in-the-Loop Controls",
            "Prompt Engineering & Output Validation",
            "Git & Modern Deployment"
        ],
        "recommended_skills": [
            "Tailwind CSS & Responsive Layouts",
            "State Management (Zustand / Redux)",
            "Safety Guardrails & Content Moderation APIs",
            "Analytics & User Feedback Loops"
        ],
        "tools_technologies": [
            "React", "TypeScript", "Tailwind CSS", "FastAPI", "Vite", "Gemini / OpenAI API", "Git"
        ],
        "example_projects": [
            "Interactive AI Career Planner with Real-Time Streaming and Human Approval",
            "Document Summarizer and Q&A System with Interactive Highlights",
            "Voice & Text AI Interview Simulator with Dynamic Feedback"
        ],
        "learning_sequence": [
            "1. Modern Responsive UI with React, TypeScript & Tailwind",
            "2. RESTful & Streaming API Integration",
            "3. AI Prompt Architecture & Pydantic Structured Outputs",
            "4. Human-in-the-Loop Review Interfaces & Optimistic UI",
            "5. Performance, Telemetry & User Experience Refinement"
        ],
        "prerequisites": ["HTML/CSS/JavaScript Foundations", "Basic Python"]
    }
]
