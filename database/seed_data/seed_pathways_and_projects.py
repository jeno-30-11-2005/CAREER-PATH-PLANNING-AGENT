# database/seed_data/seed_pathways_and_projects.py
"""
Large-Scale Career Progression Pathways & Practical Portfolio Projects Generator.
Target:
- 200+ realistic career progression pathways across all 50 career families.
- 500+ practical portfolio projects with detailed architectures, implementation steps,
  deliverables, and mapped technical skills.
"""
import os
import sys
import re

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from database.connection import get_db_session, init_db
from database.models import (
    Career, CareerCategory, CareerPathway, Project, ProjectSkill, TechnicalSkill
)

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[\s/\\+]+', '-', text)
    text = re.sub(r'[^a-z0-9\-._]', '', text)
    return text.strip('-')

# Sample project templates by family category
FAMILY_PROJECT_PATTERNS = {
    "AI": ("Autonomous Multi-Modal Reasoning Engine", "Production Microservice", 60, "Develop an end-to-end multimodal reasoning engine capable of ingesting video frames, audio transcripts, and text prompts with sub-second latency.", "Python, PyTorch Framework, FastAPI, Docker Containerization"),
    "GenAI": ("Enterprise RAG Knowledge Assistant with Citation Verification", "Portfolio Capstone", 50, "Build an enterprise document search engine utilizing semantic chunking, vector stores, and automated hallucination guardrails.", "Python, OpenAI GPT-4 API, LangChain LLM Chains, PostgreSQL"),
    "AgenticAI": ("Self-Healing Autonomous DevOps Agent with Tool Execution", "Production Microservice", 65, "Construct an autonomous AI agent capable of monitoring CI/CD build failures, inspecting stack traces, and proposing git patch fixes.", "Python, LangGraph Workflow Graphs, FastAPI, Docker Containerization"),
    "ML": ("High-Throughput Real-Time Fraud Detection Microservice", "Production Microservice", 45, "Train and deploy an XGBoost model evaluating incoming transaction batches for credit card fraud under 20ms.", "Python, Scikit-Learn, XGBoost Gradient Boosting, FastAPI"),
    "DL": ("Custom Vision Transformer (ViT) with Mixed-Precision Training", "Research Prototype", 70, "Train a vision transformer from scratch with patch tokenization, multi-head attention, and distributed GPU acceleration.", "Python, PyTorch Framework, CUDA GPU Programming, Docker Containerization"),
    "DS": ("End-to-End Customer Retention & Churn Prediction System", "Portfolio Capstone", 40, "Conduct exploratory data analysis, train predictive churn models, and present interactive risk dashboards.", "Python, Pandas Data Manipulation, Scikit-Learn, SQL (PostgreSQL)"),
    "DA": ("Executive Commercial Intelligence & Marketing Attribution Dashboard", "Guided Tutorial", 30, "Build an automated multi-touch marketing attribution model and interactive Power BI report suite.", "SQL (PostgreSQL), Power BI Desktop, Excel Advanced Functions, Python"),
    "BI": ("Enterprise Dimensional Data Mart with Automated DAX KPI Models", "Portfolio Capstone", 45, "Design a Kimball star-schema data warehouse, calculate complex DAX year-over-year metrics, and configure row-level security.", "Power BI Desktop, SQL (PostgreSQL), DAX (Data Analysis Expressions), Snowflake Cloud Data Warehouse"),
    "DE": ("Petabyte Streaming Data Pipeline with Delta Lake & Apache Spark", "Production Microservice", 55, "Ingest high-velocity clickstream event logs through Kafka into an Apache Iceberg lakehouse with automated schema validation.", "Python, Apache Spark, Kafka Distributed Streaming, Apache Airflow Workflow Orchestration"),
    "BigData": ("Distributed In-Memory Analytics Cluster with ClickHouse & Trino", "Production Microservice", 60, "Deploy an MPP analytics cluster capable of querying 500 million transaction records in under 200ms.", "ClickHouse Columnar Database, SQL (PostgreSQL), Docker Containerization, Linux CLI Core Utilities"),
    "Frontend": ("Modern Accessible Design System & Headless Component Library", "Portfolio Capstone", 40, "Build a WCAG 2.2 AA compliant React component library with Tailwind CSS, Storybook documentation, and automated tests.", "TypeScript, React.js Component Architecture, Tailwind CSS, HTML5 & Semantic Markup"),
    "Backend": ("Asynchronous Event-Driven Microservice with JWT Auth & Redis Cache", "Production Microservice", 45, "Construct high-throughput REST API endpoints with async route handlers, connection pooling, and automated Swagger specs.", "Python, FastAPI, PostgreSQL, Redis In-Memory Data Structures"),
    "FullStack": ("Full-Stack Collaborative Workspace with Real-Time WebSockets", "Portfolio Capstone", 60, "Develop a collaborative document editing platform with live cursor synchronization, markdown export, and user auth.", "TypeScript, Next.js App Router Framework, React.js Component Architecture, PostgreSQL"),
    "Mobile": ("Native Jetpack Compose / SwiftUI Offline-First Mobile Client", "Portfolio Capstone", 50, "Build a cross-platform mobile app with local SQLite caching, background bi-directional sync, and biometric unlock.", "Kotlin Programming Language, Jetpack Compose Modern UI, Android Studio IDE, Git Version Control"),
    "Cloud": ("Multi-Region High-Availability Cloud Infrastructure with Terraform", "Production Microservice", 45, "Provision a Well-Architected AWS multi-region VPC with auto-scaling compute, ALB load balancers, and RDS multi-AZ failover.", "AWS Cloud Architecture Frameworks, Terraform, Docker Containerization, Linux CLI Core Utilities"),
    "DevOps": ("Automated GitOps Kubernetes Deployment Pipeline with ArgoCD", "Production Microservice", 40, "Configure declarative continuous delivery pipelines automatically deploying microservices into Kubernetes via GitOps.", "Kubernetes Core Architecture, Docker Containerization, GitHub Actions CI/CD, Terraform"),
    "PlatformSRE": ("Distributed Observability & Chaos Resilience Testing Harness", "Production Microservice", 50, "Set up Prometheus, Grafana, and OpenTelemetry distributed tracing, then simulate node outages to verify self-healing.", "Prometheus Metrics Monitoring, Kubernetes Core Architecture, Linux CLI Core Utilities, Python"),
    "Cybersecurity": ("Enterprise Security Operations Center (SOC) Alert Triage Lab", "Guided Tutorial", 35, "Configure automated SIEM correlation rules detecting lateral movement, pass-the-hash, and exfiltration attempts.", "SIEM Operations (Splunk/Sentinel), Linux CLI Core Utilities, Computer Networking Fundamentals, Wireshark Packet Analysis"),
    "EthicalHacking": ("Authorized Web & API Penetration Testing Assessment Lab", "Portfolio Capstone", 45, "Conduct a comprehensive vulnerability assessment identifying BOLA, SQL injection, and privilege escalation vulnerabilities.", "Burp Suite Web Application Testing, OWASP Top 10 Web Vulnerabilities, Python, Linux CLI Core Utilities"),
    "NetworkSecurity": ("Zero-Trust Perimeter Firewall & Micro-Segmentation Fabric", "Production Microservice", 40, "Implement next-generation firewall rules, SSL decryption policies, and software-defined network perimeter policies.", "Next-Gen Firewalls (Palo Alto/Fortinet), Computer Networking Fundamentals, Linux CLI Core Utilities, Wireshark Packet Analysis"),
    "CloudSec": ("Automated DevSecOps Pipeline with SAST, DAST & Container Hardening", "Production Microservice", 45, "Embed automated security gates into GitHub Actions pipelines blocking pull requests with high-severity vulnerabilities.", "GitHub Actions CI/CD, Docker Containerization, Linux CLI Core Utilities, Terraform"),
    "DFIR": ("Digital Forensics Incident Response & Memory Extraction Lab", "Portfolio Capstone", 40, "Acquire disk and RAM memory images from a compromised server, extract malware persistence keys, and draft court evidence.", "Autopsy Digital Forensics Platform, Volatility Memory Forensics Framework, Linux CLI Core Utilities, Python"),
    "Blockchain": ("Layer 2 Optimistic Rollup State Sequencer Prototype", "Research Prototype", 70, "Build a prototype state transition sequencer compiling transaction batches and generating fraud verification proofs.", "Go Programming Language, Rust Systems Programming, Cryptography Fundamentals (ECC/RSA), Docker Containerization"),
    "SmartContracts": ("Audited Decentralized Lending & Liquidity Pool Protocol", "Portfolio Capstone", 55, "Write, test, and gas-profile an ERC-20 lending smart contract with collateralized borrowing and liquidation logic.", "Solidity Smart Contract Language, Foundry Smart Contract Framework, Git Version Control, TypeScript"),
    "IoT": ("Industrial IoT Sensor Telemetry Pipeline with MQTT & AWS IoT Core", "Portfolio Capstone", 45, "Connect ESP32 microcontrollers to an AWS IoT Core gateway, streaming real-time temperature telemetry to cloud databases.", "Embedded C & C++ Programming, MQTT & CoAP IoT Protocols, Python, ESP32 Wireless SoC"),
    "Robotics": ("Autonomous Mobile Robot Navigation & Obstacle Avoidance in ROS 2", "Portfolio Capstone", 60, "Program a differential drive robot in ROS 2 to autonomously navigate indoor maps using 2D LiDAR and Nav2 behaviors.", "Robot Operating System (ROS 2), C++, Python, Linux CLI Core Utilities"),
    "Embedded": ("Bare-Metal ARM Cortex-M Sensor Driver & FreeRTOS Kernel Suite", "Portfolio Capstone", 50, "Write bare-metal register drivers for I2C sensors and schedule concurrent multi-task telemetry with FreeRTOS.", "Embedded C & C++ Programming, ARM Cortex-M Architecture, FreeRTOS Real-Time Kernel, Oscilloscopes & Logic Analyzers"),
    "VLSI": ("Synthesized RISC-V ALU & Pipelined Execution Unit in Verilog", "Portfolio Capstone", 65, "Design, simulate, and verify a 32-bit pipelined ALU in Verilog with static timing closure and UVM testbenches.", "Verilog HDL, SystemVerilog Verification, Digital Logic Design & Boolean Algebra, Linux CLI Core Utilities"),
    "FPGA": ("High-Speed 10GbE Network Packet Filter Pipeline on FPGA", "Production Microservice", 60, "Implement a hardware packet processing pipeline in Verilog parsing Ethernet headers at line rate on Xilinx Vivado.", "Verilog HDL, AMD Xilinx Vivado Suite, Digital Logic Design & Boolean Algebra, C++"),
    "HardwareArch": ("Cycle-Accurate Cache Coherence & Pipeline Simulator in C++", "Research Prototype", 70, "Construct a cycle-accurate simulator modeling superscalar instruction decode, branch prediction, and MESI cache states.", "Computer Architecture Principles, C++, Digital Logic Design & Boolean Algebra, Linux CLI Core Utilities"),
    "SoftwareArch": ("Enterprise Modular Monolith with Clean Architecture & Domain-Driven Design", "Portfolio Capstone", 50, "Architect a modular enterprise backend with separated domain entities, use-case interactors, and repository interfaces.", "System Design Fundamentals, Design Patterns (GoF), Python, PostgreSQL"),
    "DistributedSys": ("Distributed Raft Consensus & Key-Value Storage Engine in Go", "Production Microservice", 65, "Implement leader election, log replication, and heartbeat mechanisms of the Raft consensus algorithm in Go.", "Go Programming Language, Distributed Consensus (Raft/Paxos), Docker Containerization, Linux CLI Core Utilities"),
    "APIEng": ("Enterprise Federated GraphQL & OpenAPI Microservice Gateway", "Production Microservice", 45, "Design an API gateway unifying federated subgraphs with automated rate-limiting, schema validation, and tracing.", "RESTful API Architecture, OpenAPI (Swagger) Specification, Python, Docker Containerization"),
    "SoftwareQA": ("Comprehensive Enterprise Test Automation & Quality Assurance Suite", "Guided Tutorial", 35, "Author a comprehensive test strategy, functional test plan, defect severity matrix, and automated regression suite.", "Manual Software Testing Methodologies, Jira & Confluence Management, Bug Tracking & Defect Life Cycle, SQL (PostgreSQL)"),
    "SDET": ("Full-Stack Playwright / TypeScript End-to-End Test Automation Framework", "Production Microservice", 45, "Build an automated testing framework with Page Object Models, auto-waiting assertions, parallelization, and CI runs.", "TypeScript, Playwright Browser Automation, Git Version Control, GitHub Actions CI/CD"),
    "UIUX": ("Comprehensive End-to-End Mobile App UI/UX Redesign & User Study", "Portfolio Capstone", 40, "Conduct user interviews, design user journey maps, build high-fidelity interactive Figma prototypes, and usability test.", "Figma Interface Design, Wireframing & Prototyping, User Journey Mapping, Qualitative User Research"),
    "ProductDesign": ("Micro-Interaction Animation System & Interactive Product Prototype", "Portfolio Capstone", 40, "Create fluid motion UI components, spring easing transitions, and interactive design prototypes in Framer.", "Figma Interface Design, ProtoPie / Framer Interactive Prototyping, Color Theory & Typography, Wireframing & Prototyping"),
    "GameDev": ("Third-Person Action Gameplay Mechanics & Character Controller", "Portfolio Capstone", 60, "Develop a third-person combat character controller in Unreal Engine 5 with combo animations and hit detection.", "Unreal Engine 5, C++, Linear Algebra & Matrix Operations, Git Version Control"),
    "SpatialComputing": ("Mixed Reality Interactive Spatial Productivity Application", "Portfolio Capstone", 55, "Build an interactive spatial app for Meta Quest or Apple Vision Pro with 6DoF hand tracking and spatial audio anchors.", "Unity Game Engine, C# Programming Language, OpenXR Cross-Platform API, Linear Algebra & Matrix Operations"),
    "GraphicsVFX": ("Physically-Based Deferred Rendering Engine in Vulkan / C++", "Research Prototype", 75, "Program a deferred renderer in Vulkan implementing PBR lighting, shadow cascades, and compute-shader post effects.", "C++, OpenGL / Vulkan Graphics APIs, Linear Algebra & Matrix Operations, HLSL / GLSL Shader Authoring"),
    "FinTech": ("Ultra-Low Latency Order Matching Engine & Market Data Gateway", "Production Microservice", 65, "Build a sub-millisecond price-time priority limit order book with multi-threaded matching in C++.", "C++, Python, Linear Algebra & Matrix Operations, SQL (PostgreSQL)"),
    "HealthTech": ("Cloud DICOM PACS Viewer & Diagnostic Contour Segmentation Tool", "Production Microservice", 50, "Build an encrypted medical image viewer rendering 3D CT scan slices with windowing and measurement overlays.", "Python, OpenCV Image Processing, DICOM & Medical PACS Systems, FastAPI"),
    "Bioinformatics": ("Automated Whole-Genome Variant Calling Pipeline in Nextflow", "Production Microservice", 50, "Develop a reproducible NGS sequencing pipeline running BWA alignment, GATK variant calling, and VEP annotations.", "Nextflow / Snakemake Workflow Engines, Linux CLI Core Utilities, Python, Docker Containerization"),
    "AutonomousVehicles": ("3D Bird's-Eye-View Camera-LiDAR Sensor Fusion Perception Pipeline", "Research Prototype", 70, "Fuse 3D LiDAR point clouds and camera feeds with Kalman filters to track surrounding vehicles in real time.", "Python, C++, PyTorch Framework, OpenCV Image Processing"),
    "AerospaceDefense": ("DO-178C Flight Control & Autopilot State Machine Simulation", "Portfolio Capstone", 60, "Implement a fly-by-wire flight control state machine in C with rigorous MC/DC safety verification.", "Embedded C & C++ Programming, DO-178C Avionics Software Lifecycle, MATLAB & Simulink Systems Modeling, Linux CLI Core Utilities"),
    "QuantumComputing": ("Variational Quantum Eigensolver (VQE) Molecular Simulator in Qiskit", "Research Prototype", 65, "Formulate molecular Hamiltonians and compute ground-state energies of small molecules on quantum circuits.", "Python, Qiskit Quantum SDK, Linear Algebra & Matrix Operations, NumPy Numerical Computing"),
    "HPC": ("Distributed MPI Parallel Solver for Navier-Stokes Fluid Equations", "Research Prototype", 65, "Parallelize a 3D fluid dynamics solver across multiple CPU cluster nodes using MPI non-blocking messages.", "C++, MPI & OpenMP Parallel Programming, Linux CLI Core Utilities, Git Version Control"),
    "SciComp": ("Finite Element Analysis Structural Solver in Python & NumPy", "Research Prototype", 55, "Code a 2D/3D truss and beam finite element solver calculating nodal displacements, strain, and stress tensors.", "Python, NumPy Numerical Computing, SciPy Scientific Algorithms, Linear Algebra & Matrix Operations"),
    "GIS": ("High-Performance Geospatial Spatial Query & Vector Tile Server", "Production Microservice", 45, "Build a web mapping service generating dynamic vector map tiles from millions of PostGIS polygons.", "PostGIS Spatial Database, Python, JavaScript (ES6+), SQL (PostgreSQL)"),
    "EmergingTech": ("Real-Time Municipal Digital Twin & IoT Telemetry Dashboard", "Portfolio Capstone", 50, "Connect city environmental sensors via MQTT to an interactive 3D digital twin dashboard displaying air quality.", "Python, MQTT & CoAP IoT Protocols, SQL (PostgreSQL), Docker Containerization")
}

def seed_pathways_and_projects(db: Session = None):
    init_db()

    def _execute(session: Session):
        print("[*] Starting Career Pathways and Portfolio Projects Seeding...")
        all_careers = session.query(Career).join(CareerCategory).all()
        career_by_title = {c.title: c for c in all_careers}
        careers_by_family = {}
        for c in all_careers:
            code = c.category.code
            if code not in careers_by_family:
                careers_by_family[code] = []
            careers_by_family[code].append(c)

        all_skills = session.query(TechnicalSkill).all()
        skill_by_name = {s.name.lower(): s for s in all_skills}

        # -------------------------------------------------------------
        # 1. SEED CAREER PATHWAYS (Target: 200+ distinct transitions)
        # -------------------------------------------------------------
        pathways_count = 0
        existing_pathways = session.query(CareerPathway).count()
        if existing_pathways == 0:
            for fam_code, c_list in careers_by_family.items():
                # Intra-family progressions (e.g. 0->1, 1->2, 2->8, etc.)
                for i in range(len(c_list) - 1):
                    start_c = c_list[i]
                    next_c = c_list[i + 1]

                    prog_type = "Vertical Promotion" if i < 3 else ("Domain Specialization" if i < 6 else "Leadership Track")
                    duration = 12 if i < 3 else (18 if i < 6 else 24)

                    pw = CareerPathway(
                        starting_career_id=start_c.career_id,
                        next_career_id=next_c.career_id,
                        progression_type=prog_type,
                        required_skills_delta=f"Advanced competencies in {next_c.subcategory} and systems leadership.",
                        additional_learning=f"Industry certifications in {next_c.recommended_certifications or 'advanced engineering'}.",
                        recommended_projects=f"Lead an enterprise production deployment in {next_c.title}.",
                        estimated_duration_months=duration,
                        preparation_guidelines=f"Transition from operational execution to system architecture, mentoring junior engineers, and leading technical design reviews.",
                        verification_status="Verified"
                    )
                    session.add(pw)
                    pathways_count += 1

                # Inter-family lateral transitions (e.g., career i -> related domain)
                if fam_code == "Frontend" and "FullStack" in careers_by_family:
                    target = careers_by_family["FullStack"][0]
                    session.add(CareerPathway(
                        starting_career_id=c_list[0].career_id,
                        next_career_id=target.career_id,
                        progression_type="Lateral Transition",
                        required_skills_delta="Backend API architecture, databases, and containerization.",
                        additional_learning="PostgreSQL, FastAPI, Docker, and distributed caching.",
                        recommended_projects="Full-stack real-time collaboration application.",
                        estimated_duration_months=12,
                        preparation_guidelines="Expand frontend component mastery into full-lifecycle server development.",
                        verification_status="Verified"
                    ))
                    pathways_count += 1

                if fam_code == "DA" and "DS" in careers_by_family:
                    target = careers_by_family["DS"][0]
                    session.add(CareerPathway(
                        starting_career_id=c_list[0].career_id,
                        next_career_id=target.career_id,
                        progression_type="Lateral Transition",
                        required_skills_delta="Machine learning algorithms, advanced statistics, and predictive modeling.",
                        additional_learning="Scikit-Learn, hypothesis testing, feature engineering.",
                        recommended_projects="End-to-end customer churn prediction pipeline.",
                        estimated_duration_months=12,
                        preparation_guidelines="Transition from diagnostic SQL querying to predictive statistical modeling.",
                        verification_status="Verified"
                    ))
                    pathways_count += 1

                if fam_code == "ML" and "AI" in careers_by_family:
                    target = careers_by_family["AI"][0]
                    session.add(CareerPathway(
                        starting_career_id=c_list[0].career_id,
                        next_career_id=target.career_id,
                        progression_type="Domain Specialization",
                        required_skills_delta="Novel neural architectures, tensor optimization, and deep learning research.",
                        additional_learning="Transformer mechanics, GPU CUDA programming, mathematical optimization.",
                        recommended_projects="Custom multi-head attention transformer trained from scratch.",
                        estimated_duration_months=18,
                        preparation_guidelines="Deepen theoretical mathematics and contribute to open-source foundation model research.",
                        verification_status="Verified"
                    ))
                    pathways_count += 1

                if fam_code == "Cybersecurity" and "EthicalHacking" in careers_by_family:
                    target = careers_by_family["EthicalHacking"][0]
                    session.add(CareerPathway(
                        starting_career_id=c_list[0].career_id,
                        next_career_id=target.career_id,
                        progression_type="Offensive Transition",
                        required_skills_delta="Offensive penetration testing, Burp Suite, exploit payloads, and evasion.",
                        additional_learning="OSCP certification, web app security testing, Active Directory attacks.",
                        recommended_projects="Complete 30 advanced vulnerable machine challenges on HackTheBox.",
                        estimated_duration_months=12,
                        preparation_guidelines="Shift from defensive alert triage to adversarial attack mindset.",
                        verification_status="Verified"
                    ))
                    pathways_count += 1

            session.flush()
            print(f"[PATHWAYS SUCCESS] Seeded {pathways_count} distinct career progression pathways!")
        else:
            pathways_count = existing_pathways
            print(f"[PATHWAYS INFO] {pathways_count} pathways already present in database.")

        # -------------------------------------------------------------
        # 2. SEED PRACTICAL PORTFOLIO PROJECTS (Target: 500+ projects)
        # -------------------------------------------------------------
        projects_count = 0
        existing_projects = session.query(Project).count()
        if existing_projects == 0:
            for career in all_careers:
                fam_code = career.category.code
                pattern = FAMILY_PROJECT_PATTERNS.get(fam_code, (
                    f"Production Enterprise {career.title} Solution",
                    "Portfolio Capstone",
                    45,
                    f"Develop a complete, production-grade project demonstrating core proficiencies in {career.title}.",
                    "Python, Docker Containerization, Git Version Control, SQL (PostgreSQL)"
                ))

                p_title = f"{career.title}: {pattern[0]}"
                p_type = pattern[1]
                p_hours = pattern[2]
                p_problem = pattern[3]
                p_tech = pattern[4]

                project = Project(
                    title=p_title[:150],
                    career_id=career.career_id,
                    category=career.category.name,
                    difficulty=career.difficulty_level,
                    estimated_hours=p_hours,
                    project_type=p_type,
                    problem_statement=p_problem,
                    objective=f"Build and deploy an enterprise-grade portfolio project proving real-world readiness for {career.title}.",
                    description=f"A comprehensive practical capstone project covering the core workflows, technical stack, and architecture of a professional {career.title}.",
                    suggested_technologies=p_tech,
                    implementation_steps=(
                        "Step 1: System architecture design, database schema, and interface contracts.\n"
                        "Step 2: Core backend engine development and integration of essential dependencies.\n"
                        "Step 3: Automated unit and integration testing with test fixtures.\n"
                        "Step 4: Containerization with Docker and deployment onto cloud infrastructure."
                    ),
                    expected_deliverables=(
                        "1. Clean, documented GitHub repository with complete README and architecture diagrams.\n"
                        "2. Containerized runnable application with Dockerfile and environment configs.\n"
                        "3. Automated test suite achieving >80% code coverage.\n"
                        "4. Live demo URL or recorded video walkthrough."
                    ),
                    learning_outcomes=f"Hands-on mastery of {career.title} engineering paradigms, industry best practices, and portfolio-ready code.",
                    suggested_extensions="Implement distributed caching, OAuth2 security, and automated CI/CD deployment pipelines."
                )
                session.add(project)
                session.flush()
                projects_count += 1

                # Map ProjectSkills
                for tech_name in [t.strip() for t in p_tech.split(",")]:
                    sk = skill_by_name.get(tech_name.lower())
                    if sk:
                        session.add(ProjectSkill(
                            project_id=project.project_id,
                            skill_id=sk.skill_id
                        ))

            session.commit()
            print(f"[PROJECTS SUCCESS] Seeded {projects_count} practical portfolio projects with mapped technical skills!")
        else:
            projects_count = existing_projects
            print(f"[PROJECTS INFO] {projects_count} projects already present in database.")

        return pathways_count, projects_count

    if db is not None:
        return _execute(db)
    else:
        with get_db_session() as session:
            return _execute(session)

if __name__ == "__main__":
    pw_c, pr_c = seed_pathways_and_projects()
    print(f"\n[PHASE 8 SUCCESS] Database now contains {pw_c} Career Pathways and {pr_c} Portfolio Projects!")
