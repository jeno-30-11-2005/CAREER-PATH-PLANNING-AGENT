# career_data.py
# Purpose: Stores career knowledge base using standard Python dictionaries and lists.
# No database required - easy to understand, edit, and explain during college viva.

CAREER_DATABASE = {
    "AI Engineer": {
        "title": "AI Engineer",
        "description": "Develops intelligent applications using Artificial Intelligence, Foundation Models, and conversational agents.",
        "related_interests": [
            "Artificial Intelligence",
            "Generative AI",
            "Robotics",
            "Natural Language Processing",
            "Deep Learning"
        ],
        "required_skills": [
            "Python",
            "Prompt Engineering",
            "FastAPI",
            "Vector Databases",
            "Deep Learning Basics",
            "Git & GitHub"
        ],
        "roadmap": [
            {
                "step": "Step 1: Foundations",
                "topics": "Python programming syntax, object-oriented programming (OOP), and Git version control.",
                "duration": "Weeks 1 - 3",
                "milestone": "Build 5 basic Python console applications and push code to GitHub."
            },
            {
                "step": "Step 2: Core AI Concepts",
                "topics": "Prompt engineering, tokenization, embeddings, and connecting to AI APIs.",
                "duration": "Weeks 4 - 6",
                "milestone": "Create an AI text summarizer using modern AI API endpoints."
            },
            {
                "step": "Step 3: Web Integration & Vector Search",
                "topics": "FastAPI backend development, REST APIs, and vector databases (ChromaDB).",
                "duration": "Weeks 7 - 9",
                "milestone": "Build a simple Document Q&A assistant with custom notes."
            },
            {
                "step": "Step 4: Portfolio & Viva Preparation",
                "topics": "Model evaluation, ethical AI guardrails, system documentation, and presentation prep.",
                "duration": "Weeks 10 - 12",
                "milestone": "Complete project documentation, GitHub README, and viva presentation slides."
            }
        ]
    },
    "ML Engineer": {
        "title": "Machine Learning Engineer",
        "description": "Designs and trains predictive machine learning models to solve business and classification problems.",
        "related_interests": [
            "Machine Learning",
            "Mathematics & Statistics",
            "Predictive Modeling",
            "Artificial Intelligence"
        ],
        "required_skills": [
            "Python",
            "Linear Algebra & Statistics",
            "NumPy & Pandas",
            "Scikit-Learn",
            "Data Preprocessing",
            "Model Evaluation"
        ],
        "roadmap": [
            {
                "step": "Step 1: Mathematical Foundations",
                "topics": "Linear algebra, basic probability, statistics, and Python fundamentals.",
                "duration": "Weeks 1 - 3",
                "milestone": "Implement matrix operations and statistical calculations in Python."
            },
            {
                "step": "Step 2: Data Wrangling & Analysis",
                "topics": "Data cleaning with Pandas, array manipulations with NumPy, and EDA charts.",
                "duration": "Weeks 4 - 6",
                "milestone": "Perform exploratory data analysis on a public Kaggle dataset."
            },
            {
                "step": "Step 3: Supervised & Unsupervised ML",
                "topics": "Linear regression, decision trees, random forests, clustering, and Scikit-Learn.",
                "duration": "Weeks 7 - 9",
                "milestone": "Train, evaluate, and tune a student performance predictor model."
            },
            {
                "step": "Step 4: Model Deployment & Portfolio",
                "topics": "Saving models with Joblib/Pickle, creating a Streamlit demo UI, and viva practice.",
                "duration": "Weeks 10 - 12",
                "milestone": "Deploy interactive ML predictor web app and prepare viva flashcards."
            }
        ]
    },
    "Data Analyst": {
        "title": "Data Analyst",
        "description": "Analyzes raw data, writes SQL queries, and builds visual dashboards to help organizations make informed decisions.",
        "related_interests": [
            "Data Visualization",
            "Business Analytics",
            "Database Querying",
            "Spreadsheets & Reporting"
        ],
        "required_skills": [
            "SQL (Queries, Joins, GroupBy)",
            "Excel / Spreadsheets",
            "Python (Pandas & Matplotlib)",
            "PowerBI / Tableau",
            "Business Communication",
            "Exploratory Data Analysis"
        ],
        "roadmap": [
            {
                "step": "Step 1: Excel & Database Fundamentals",
                "topics": "Advanced Excel (VLOOKUP, Pivot Tables) and relational database concepts.",
                "duration": "Weeks 1 - 3",
                "milestone": "Analyze a retail sales spreadsheet and summarize findings in charts."
            },
            {
                "step": "Step 2: SQL Data Querying",
                "topics": "SELECT queries, WHERE filtering, INNER/LEFT joins, GROUP BY, and aggregates.",
                "duration": "Weeks 4 - 6",
                "milestone": "Write 20 complex SQL queries answering practical business questions."
            },
            {
                "step": "Step 3: Python Data Visualization",
                "topics": "Pandas data wrangling, bar charts, line plots, and distributions using Matplotlib/Seaborn.",
                "duration": "Weeks 7 - 9",
                "milestone": "Build an exploratory data analysis notebook with visual charts."
            },
            {
                "step": "Step 4: Interactive Dashboards & Viva",
                "topics": "Building interactive dashboards (PowerBI/Streamlit) and presentation storytelling.",
                "duration": "Weeks 10 - 12",
                "milestone": "Publish an interactive sales analytics dashboard and rehearse project presentation."
            }
        ]
    },
    "Python Developer": {
        "title": "Python Developer",
        "description": "Constructs robust software applications, REST APIs, and backend services using the Python programming language.",
        "related_interests": [
            "Software Development",
            "Web Development",
            "Backend Systems",
            "Automation Scripting"
        ],
        "required_skills": [
            "Python",
            "Object-Oriented Programming",
            "REST APIs (FastAPI / Flask)",
            "Relational Databases (SQL)",
            "Git & Version Control",
            "Unit Testing"
        ],
        "roadmap": [
            {
                "step": "Step 1: Core Python & Algorithms",
                "topics": "Control flow, functions, data structures (lists, dicts, sets), and OOP classes.",
                "duration": "Weeks 1 - 3",
                "milestone": "Create an object-oriented student management system in console."
            },
            {
                "step": "Step 2: Database & File Handling",
                "topics": "Connecting Python to SQLite/PostgreSQL, CRUD operations, and reading JSON/CSV files.",
                "duration": "Weeks 4 - 6",
                "milestone": "Build a database-backed task manager application."
            },
            {
                "step": "Step 3: Web APIs & Frameworks",
                "topics": "Building RESTful endpoints with FastAPI or Flask, request validation, and routing.",
                "duration": "Weeks 7 - 9",
                "milestone": "Develop and test a CRUD REST API with Swagger documentation."
            },
            {
                "step": "Step 4: Testing & Project Defense",
                "topics": "Writing unit tests with Pytest, Git workflow, code modularity, and viva prep.",
                "duration": "Weeks 10 - 12",
                "milestone": "Deploy project on a free hosting platform and prepare viva explanation."
            }
        ]
    }
}

# Master list of selectable skills and interests for the UI
AVAILABLE_SKILLS = [
    "Python",
    "SQL (Queries, Joins, GroupBy)",
    "NumPy & Pandas",
    "Scikit-Learn",
    "Linear Algebra & Statistics",
    "Data Preprocessing",
    "Model Evaluation",
    "Prompt Engineering",
    "FastAPI",
    "Vector Databases",
    "Deep Learning Basics",
    "Excel / Spreadsheets",
    "PowerBI / Tableau",
    "Business Communication",
    "Exploratory Data Analysis",
    "Object-Oriented Programming",
    "REST APIs (FastAPI / Flask)",
    "Git & Version Control",
    "Unit Testing"
]

AVAILABLE_INTERESTS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Generative AI",
    "Data Visualization",
    "Business Analytics",
    "Software Development",
    "Web Development",
    "Backend Systems",
    "Automation Scripting",
    "Mathematics & Statistics",
    "Database Querying",
    "Natural Language Processing"
]
