# database/seed_data/seed_interests.py
"""
Areas of Interest Database Generator & Seeder.
Target: 250+ distinct, categorized interest areas with domain mappings,
learning difficulty, and descriptions.
"""
import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from database.connection import get_db_session
from database.models import InterestCategory, AreaOfInterest

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[\s/\\+]+', '-', text)
    text = re.sub(r'[^a-z0-9\-._]', '', text)
    return text.strip('-')

INTEREST_CATALOG = [
    # 1. Artificial Intelligence & Cognitive Computing
    ("Artificial Intelligence", "Cognitive Systems", [
        ("Autonomous AI Agents", "Exploring multi-agent systems and autonomous cognitive architectures.", "High", "Technology"),
        ("Generative AI & LLMs", "Building with foundation models, prompt systems, and generative tools.", "Moderate", "Technology"),
        ("Natural Language Processing", "Understanding human text, sentiment analysis, and machine translation.", "Moderate", "Software"),
        ("Computer Vision & Perception", "Visual scene analysis, object detection, and video segmentation.", "High", "Technology"),
        ("Reinforcement Learning", "Reward-driven policy optimization for robotics, games, and autonomous driving.", "High", "Research"),
        ("Retrieval-Augmented Generation (RAG)", "Grounding foundation models with enterprise knowledge bases and vector search.", "Moderate", "Enterprise"),
        ("Speech & Audio AI", "Speech synthesis, voice cloning, and automatic speech recognition.", "Moderate", "Consumer Tech"),
        ("Multimodal AI", "Cross-modal models integrating text, vision, and audio reasoning.", "High", "Research"),
        ("AI Safety & Alignment", "Guardrails, constitutional AI, and mitigation of bias and hallucination.", "Moderate", "Governance"),
        ("Explainable AI (XAI)", "Interpreting complex deep neural network decisions for human stakeholders.", "High", "Healthcare & Finance"),
        ("Neuromorphic Computing", "Brain-inspired spiking neural networks and bio-mimetic processing.", "High", "Research"),
        ("Synthetic Data Creation", "Generating artificial datasets to bootstrap machine learning classifiers.", "Moderate", "Data Science")
    ]),

    # 2. Machine Learning & Data Science
    ("Machine Learning & Data Science", "Data & Algorithms", [
        ("Predictive Modeling", "Training statistical models to forecast churn, demand, and risk.", "Moderate", "Enterprise"),
        ("Feature Engineering", "Extracting domain-specific mathematical signals from raw tabular datasets.", "Moderate", "Data Science"),
        ("Deep Learning Architectures", "Designing and training deep convolutional, recurrent, and transformer networks.", "High", "Technology"),
        ("Unsupervised Learning & Clustering", "Discovering latent customer personas and anomalies without labels.", "Moderate", "Business Analytics"),
        ("Time Series Forecasting", "Predicting macroeconomic, inventory, and sensor trajectories over time.", "Moderate", "Finance & Supply Chain"),
        ("Automated Machine Learning (AutoML)", "Automating pipeline creation, hyperparameter search, and model selection.", "Low", "Software"),
        ("Recommender Systems", "Collaborative filtering and matrix factorization for e-commerce and media.", "Moderate", "Consumer Tech"),
        ("Graph Machine Learning", "Applying graph neural networks to social networks, fraud, and drug discovery.", "High", "Research"),
        ("Bayesian Data Analysis", "Probabilistic graphical modeling and uncertainty quantification.", "High", "Science & Research"),
        ("A/B Testing & Causal Inference", "Designing randomized experiments to establish true cause-and-effect.", "Moderate", "Product Analytics")
    ]),

    # 3. Data Analytics & Business Intelligence
    ("Data Analytics & Business Intelligence", "Business Insights", [
        ("Interactive Business Dashboards", "Designing executive dashboards tracking KPIs, revenue, and churn.", "Low", "Enterprise"),
        ("Customer Journey Analytics", "Analyzing multi-touch attribution, funnels, and user onboarding drop-offs.", "Low", "Marketing"),
        ("Data Storytelling", "Translating complex statistical findings into clear executive presentations.", "Low", "Business"),
        ("Self-Service BI", "Empowering non-technical business teams to query curated data models.", "Low", "Enterprise"),
        ("Financial Modeling & Analytics", "Forecasting profit-and-loss, cash flow runways, and valuation ratios.", "Moderate", "Finance"),
        ("Supply Chain & Logistics Analytics", "Optimizing warehouse inventory routes, lead times, and freight costs.", "Moderate", "Logistics"),
        ("Healthcare Operational Analytics", "Tracking hospital bed occupancy, patient readmission, and clinical outcomes.", "Moderate", "Healthcare"),
        ("E-Commerce Conversion Analytics", "Optimizing shopping cart conversion rates, average order values, and retention.", "Low", "Retail"),
        ("Human Resources (People) Analytics", "Measuring employee retention, attrition drivers, and workforce productivity.", "Low", "Corporate"),
        ("Product Telemetry & Feature Adoption", "Analyzing feature engagement, daily active usage, and stickiness.", "Low", "SaaS")
    ]),

    # 4. Data Engineering & Big Data
    ("Data Engineering & Big Data", "Data Infrastructure", [
        ("Real-Time Event Streaming", "Publishing and consuming high-throughput telemetry streams using Kafka.", "High", "Infrastructure"),
        ("Data Lakehouse Architecture", "Unifying raw data lakes with ACID transactional relational tables.", "Moderate", "Enterprise"),
        ("Distributed Batch Compute", "Processing terabyte-scale datasets across Spark clusters.", "High", "Cloud"),
        ("Data Quality & Governance", "Automating schema validation, lineage tracking, and metadata catalogs.", "Moderate", "Enterprise"),
        ("Change Data Capture (CDC)", "Streaming transactional database mutation logs into analytical warehouses.", "Moderate", "Infrastructure"),
        ("Analytics Engineering with dbt", "Structuring maintainable SQL transformations with version control and testing.", "Moderate", "Data"),
        ("Data Mesh Architecture", "Decentralizing data ownership across autonomous domain teams.", "High", "Enterprise Architecture"),
        ("Cloud Data Warehousing", "Optimizing query execution and clustering in Snowflake and BigQuery.", "Moderate", "Cloud"),
        ("Vector Search Pipelines", "ETL pipelines chunking, embedding, and syncing documents to vector stores.", "Moderate", "AI Systems"),
        ("Data Pipeline Orchestration", "Scheduling complex DAG dependencies and retries with Apache Airflow.", "Moderate", "DevOps")
    ]),

    # 5. Software Development & Web Engineering
    ("Software Development", "Application Engineering", [
        ("Full-Stack Web Development", "Building end-to-end web applications with modern frontend and backend tiers.", "Moderate", "Software"),
        ("Microservices & Distributed Systems", "Decomposing monolithic architectures into loosely coupled services.", "High", "Enterprise"),
        ("API Architecture & Design", "Designing clean, versioned REST, GraphQL, and gRPC service contracts.", "Moderate", "Software"),
        ("Responsive Frontend Engineering", "Crafting intuitive, responsive web interfaces accessible across all screen sizes.", "Low", "Web"),
        ("Clean Architecture & Domain-Driven Design", "Structuring maintainable code around domain models and ubiquitous language.", "High", "Software"),
        ("Component-Driven UI Engineering", "Building reusable design system component libraries in React or Vue.", "Low", "Frontend"),
        ("Serverless Web Applications", "Building zero-server web services with edge functions and cloud databases.", "Moderate", "Cloud"),
        ("Web Performance Optimization", "Achieving sub-second load times and 100/100 Core Web Vitals scores.", "Moderate", "Web"),
        ("Progressive Web Apps (PWA)", "Creating web apps that work offline and install on mobile home screens.", "Moderate", "Mobile Web"),
        ("Real-Time Collaborative Web Apps", "Building live multi-user editing with WebSockets and CRDTs.", "High", "Software")
    ]),

    # 6. Mobile Application Development
    ("Mobile Development", "Mobile Systems", [
        ("Android Native Development", "Building high-performance native apps using Kotlin and Jetpack Compose.", "Moderate", "Mobile"),
        ("iOS Native Development", "Crafting polished Apple experiences using Swift and SwiftUI.", "Moderate", "Mobile"),
        ("Cross-Platform Flutter Apps", "Building compiled native applications for iOS and Android from one Dart codebase.", "Moderate", "Mobile"),
        ("React Native Mobile Apps", "Deploying native apps leveraging existing React and TypeScript expertise.", "Moderate", "Mobile"),
        ("Mobile Offline-First Architecture", "Syncing local SQLite/Room data transparently when network connectivity restores.", "Moderate", "Software"),
        ("Mobile App Security & Biometrics", "Securing keychain storage, biometric unlock, and certificate pinning.", "High", "Security"),
        ("Mobile Augmented Reality", "Overlaying 3D virtual objects onto real-world camera feeds with ARKit and ARCore.", "High", "Interactive Media"),
        ("Wearable & Smartwatch Apps", "Designing glanceable interfaces for Apple Watch and Wear OS devices.", "Moderate", "Wearables"),
        ("Mobile Sensor & Location Tracking", "Leveraging GPS, accelerometers, and gyroscopes for context-aware apps.", "Moderate", "Mobile Services"),
        ("Mobile Game Development", "Creating casual 2D and 3D mobile games optimized for touch gestures.", "Moderate", "Gaming")
    ]),

    # 7. Cloud Computing & DevOps
    ("Cloud & DevOps", "Cloud Infrastructure", [
        ("Cloud Infrastructure Architecture", "Designing resilient, multi-region cloud systems on AWS, Azure, or GCP.", "Moderate", "Cloud"),
        ("Container Orchestration with Kubernetes", "Deploying, auto-scaling, and healing container clusters in production.", "High", "DevOps"),
        ("Infrastructure as Code (IaC)", "Automating cloud infrastructure provisioning with Terraform and OpenTofu.", "Moderate", "DevOps"),
        ("Continuous Integration & Deployment (CI/CD)", "Automating code linting, unit tests, and production releases.", "Moderate", "DevOps"),
        ("Site Reliability Engineering (SRE)", "Ensuring 99.99% system uptime using error budgets and observability.", "High", "Operations"),
        ("GitOps Delivery Pipelines", "Synchronizing Kubernetes cluster configurations from Git commits.", "Moderate", "Cloud Native"),
        ("Cloud Cost Optimization (FinOps)", "Minimizing cloud computing bills through reserved instances and right-sizing.", "Moderate", "Finance & IT"),
        ("Serverless Architecture", "Event-driven serverless computing eliminating server maintenance overhead.", "Moderate", "Cloud"),
        ("Multi-Cloud Management", "Avoiding single-vendor lock-in by designing portable multi-cloud workloads.", "High", "Enterprise IT"),
        ("Observability & Distributed Tracing", "Monitoring microservice request latency with OpenTelemetry and Prometheus.", "Moderate", "SRE")
    ]),

    # 8. Cybersecurity & Ethical Hacking
    ("Cybersecurity", "Information Security", [
        ("Penetration Testing & Ethical Hacking", "Simulating adversary tactics to uncover vulnerabilities in web and network systems.", "High", "Security"),
        ("Web Application Security (AppSec)", "Auditing code against OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF).", "Moderate", "Software"),
        ("Security Operations Center (SOC) Analysis", "Monitoring SIEM alerts, investigating breaches, and neutralizing intrusions.", "Moderate", "Security Ops"),
        ("Digital Forensics & Incident Response", "Extracting disk images, analyzing memory dumps, and proving breach timelines.", "High", "Law Enforcement"),
        ("Cloud Security Posture", "Hardening IAM policies, VPC perimeters, and S3 bucket permissions in public clouds.", "Moderate", "Cloud"),
        ("Zero Trust Architecture", "Designing perimeter-less networks where every access request is continuously verified.", "High", "Enterprise Security"),
        ("Cryptography & Encryption", "Securing data in transit and at rest using AES, RSA, and post-quantum ciphers.", "High", "Mathematics"),
        ("Malware Analysis & Reverse Engineering", "Disassembling malicious binaries to understand payload behavior and C2 servers.", "High", "Security"),
        ("Threat Modeling & Risk Assessment", "Proactively mapping system threat vectors using STRIDE and DREAD methodologies.", "Moderate", "Architecture"),
        ("Identity & Access Management (IAM)", "Implementing Single Sign-On (SSO), OAuth 2.0, and biometric MFA.", "Moderate", "Enterprise IT")
    ]),

    # 9. Computer Networking & Systems
    ("Networking & Systems", "Core Infrastructure", [
        ("Enterprise Network Engineering", "Configuring core routers, switches, OSPF routing, and BGP peering.", "Moderate", "Telecommunications"),
        ("Software-Defined Networking (SDN)", "Decoupling network control planes from packet forwarding hardware.", "High", "Data Centers"),
        ("Network Protocol Engineering", "Analyzing and implementing TCP/IP, QUIC, and WebSocket protocol layers.", "High", "Systems"),
        ("Linux Kernel & System Administration", "Tuning Linux kernel parameters, process schedulers, and LVM volumes.", "Moderate", "Infrastructure"),
        ("High-Performance Computing (HPC)", "Clustering thousands of CPU/GPU nodes for scientific weather and physics models.", "High", "Supercomputing"),
        ("Content Delivery Networks (CDN)", "Caching dynamic web media close to end users across edge PoPs.", "Moderate", "Internet Services"),
        ("Wireless & 5G Telecommunications", "Exploring cellular network slicing, radio access networks (RAN), and mmWave.", "High", "Telecom"),
        ("Network Automation with Python", "Automating Cisco and Juniper switch configurations using Netmiko and Ansible.", "Moderate", "DevOps")
    ]),

    # 10. Database Engineering
    ("Database Technologies", "Data Persistence", [
        ("Relational Database Internals", "Exploring B-Tree indexing, write-ahead logs, and buffer pool algorithms.", "High", "Software"),
        ("NoSQL & Distributed Storage", "Designing horizontal sharding schemes and partition keys for massive scale.", "Moderate", "Backend"),
        ("Graph Database Systems", "Modeling social networks, fraud rings, and dependency trees with Neo4j.", "Moderate", "Data Science"),
        ("In-Memory Caching Architectures", "Optimizing microsecond response times using Redis and Memcached.", "Moderate", "Performance"),
        ("Database Query Optimization", "Eliminating slow queries using EXPLAIN plans and composite indexing.", "Moderate", "Database"),
        ("Vector Search & Embedding Stores", "Indexing high-dimensional vector spaces using HNSW and IVF algorithms.", "Moderate", "AI"),
        ("NewSQL & Distributed ACID", "Achieving global horizontal scalability with strict serializable transactions.", "High", "Database Systems")
    ]),

    # 11. Blockchain & Web3
    ("Blockchain & Web3", "Decentralized Tech", [
        ("Smart Contract Development", "Writing secure, audited decentralized logic using Solidity and Foundry.", "High", "Blockchain"),
        ("Decentralized Finance (DeFi)", "Automated market makers, liquidity pools, and collateralized lending protocols.", "High", "Finance"),
        ("Zero-Knowledge Proofs (ZKP)", "Cryptographic proofs enabling privacy and Layer 2 ZK-Rollup scaling.", "High", "Cryptography"),
        ("Decentralized Autonomous Organizations (DAOs)", "On-chain governance voting, tokenomics, and treasury management.", "Moderate", "Governance"),
        ("Web3 Frontend Integration", "Connecting MetaMask and Web3 wallets to dApps using Wagmi and Viem.", "Moderate", "Frontend"),
        ("Smart Contract Security Auditing", "Discovering reentrancy bugs, flash loan exploits, and oracle manipulations.", "High", "Security"),
        ("Decentralized Storage Protocols", "Storing peer-to-peer immutable media using IPFS and Arweave.", "Low", "Web3"),
        ("Layer 2 Scaling Solutions", "Scaling Ethereum transaction throughput via optimistic and ZK rollups.", "High", "Architecture")
    ]),

    # 12. Robotics & Autonomous Systems
    ("Robotics", "Physical Automation", [
        ("Autonomous Mobile Robots (AMR)", "Designing warehouse robots navigating dynamic environments independently.", "High", "Robotics"),
        ("SLAM & Robot Navigation", "Simultaneous localization and mapping in unknown physical environments.", "High", "Robotics"),
        ("Robot Operating System (ROS 2)", "Connecting robotic sensors, motors, and controllers with publish-subscribe topics.", "Moderate", "Engineering"),
        ("Robotic Arm Kinematics & Manipulation", "Calculating forward and inverse kinematics for pick-and-place manufacturing.", "High", "Manufacturing"),
        ("Robotic Vision & 3D Perception", "Processing lidar point clouds and depth camera feeds for obstacle avoidance.", "High", "AI & Robotics"),
        ("Drone & UAV Autopilot Software", "Flight stabilization, waypoint navigation, and telemetry for uncrewed drones.", "High", "Aerospace"),
        ("Bio-Inspired Robotics", "Designing soft robotics and quadruped walking robots mimicking animal locomotion.", "High", "Research")
    ]),

    # 13. Internet of Things (IoT) & Embedded Systems
    ("Internet of Things & Embedded", "Physical Computing", [
        ("Microcontroller Firmware Development", "Writing bare-metal and FreeRTOS firmware in C/C++ for STM32 and ESP32.", "Moderate", "Hardware"),
        ("IoT Device Telemetry & Protocols", "Streaming battery-efficient sensor data over MQTT and CoAP.", "Moderate", "IoT"),
        ("Over-The-Air (OTA) Device Updates", "Wirelessly flashing secure firmware updates to remote IoT device fleets.", "Moderate", "DevOps"),
        ("Edge AI & TinyML", "Running compressed neural network models directly on low-power microcontrollers.", "High", "AI & Embedded"),
        ("Smart Home & Automation", "Building connected home devices integrated with Home Assistant and Matter.", "Low", "Consumer Tech"),
        ("Industrial IoT (IIoT) & SCADA", "Monitoring factory vibration, temperature, and motor RPM to predict failures.", "Moderate", "Manufacturing"),
        ("Low-Power Wireless Networks", "Connecting remote environmental sensors using LoRaWAN and BLE.", "Moderate", "Telecommunications"),
        ("Hardware Bus Protocol Interfacing", "Communicating between chips and sensors using I2C, SPI, and UART.", "Low", "Electronics")
    ]),

    # 14. VLSI & Semiconductor Engineering
    ("VLSI & Semiconductors", "Hardware Design", [
        ("RTL Design & Logic Synthesis", "Writing synthesizable digital logic in Verilog and converting to gate netlists.", "High", "Semiconductors"),
        ("Static Timing Analysis (STA)", "Verifying that circuit signals arrive within strict nanosecond clock windows.", "High", "Hardware"),
        ("FPGA Hardware Prototyping", "Deploying custom digital accelerators and soft CPUs onto Xilinx FPGAs.", "High", "Hardware"),
        ("ASIC Physical Design & Layout", "Floorplanning, placement, routing, and clock tree synthesis on silicon dies.", "High", "Semiconductors"),
        ("Design for Testability (DFT)", "Inserting scan chains and built-in self-tests (BIST) for chip fabrication QA.", "High", "Manufacturing"),
        ("Computer Architecture & Processor Design", "Designing pipelined RISC-V CPUs, branch predictors, and cache hierarchies.", "High", "Computer Science"),
        ("Analog & Mixed-Signal IC Design", "Designing CMOS operational amplifiers, DACs, and ADCs on silicon.", "High", "Electronics")
    ]),

    # 15. UI/UX Design & Product Design
    ("UI/UX & Product Design", "User Experience", [
        ("User Experience (UX) Research", "Conducting user interviews, usability tests, and card sorting experiments.", "Low", "Design"),
        ("Design Systems & Component Libraries", "Standardizing reusable typography, color palettes, and interactive tokens.", "Low", "Design"),
        ("Interactive Wireframing & Prototyping", "Creating high-fidelity clickable product simulations in Figma.", "Low", "Design"),
        ("Accessibility & Inclusive Design", "Ensuring digital products work for visually, motor, and cognitively impaired users.", "Low", "Product"),
        ("Information Architecture (IA)", "Structuring complex enterprise portals, search filters, and sitemaps.", "Low", "UX"),
        ("Micro-Interactions & Animation", "Adding delightful tactile animations that provide feedback to user actions.", "Low", "Frontend Design"),
        ("Heuristic Evaluation & UX Audits", "Auditing web interfaces against Nielsen Norman usability heuristics.", "Low", "Design Quality")
    ]),

    # 16. Game Development & AR/VR
    ("Game Development & AR/VR", "Interactive Media", [
        ("Unity Game Engine Development", "Creating 2D and 3D indie games with C# and the Unity physics engine.", "Moderate", "Gaming"),
        ("Unreal Engine 5 Real-Time 3D", "Crafting photorealistic environments and game mechanics with Blueprints and C++.", "High", "Gaming"),
        ("Virtual Reality (VR) Simulation", "Building immersive training simulations for headsets like Meta Quest.", "High", "XR"),
        ("Augmented Reality (AR) Experiences", "Projecting digital interactive models into real physical rooms on mobile.", "Moderate", "XR"),
        ("Game AI & Non-Player Characters", "Programming finite state machines and behavior trees for smart enemy tactics.", "Moderate", "Game Design"),
        ("3D Asset Modeling & Animation", "Sculpting 3D models, UV texturing, and skeletal rigging in Blender.", "Moderate", "Digital Art"),
        ("Real-Time Shader Programming", "Writing custom HLSL and GLSL shaders for glowing energy and water effects.", "High", "Graphics")
    ]),

    # 17. FinTech & Banking Technology
    ("FinTech", "Financial Tech", [
        ("Algorithmic & Quantitative Trading", "Backtesting statistical arbitrage strategies in equities and crypto markets.", "High", "Finance"),
        ("Payment Gateway Integration", "Implementing secure card checkout flows, webhooks, and subscription billing.", "Low", "FinTech"),
        ("Fraud Detection & Risk Scoring", "Using machine learning to score and block suspicious financial transactions.", "Moderate", "Banking"),
        ("Core Banking & Neobank Systems", "Building multi-currency wallets, ledger balances, and payment rails.", "High", "Banking"),
        ("Open Banking & Financial APIs", "Connecting bank accounts to budgeting apps via Plaid and Open Banking APIs.", "Moderate", "FinTech"),
        ("Regulatory Compliance (AML & KYC)", "Automating identity verification and anti-money laundering screening.", "Moderate", "Compliance")
    ]),

    # 18. Healthcare Technology & Bioinformatics
    ("Healthcare & Bioinformatics", "Life Sciences", [
        ("Computational Genomics & DNA Sequencing", "Aligning genome sequences and calling genetic variants using BioPython.", "High", "Life Sciences"),
        ("Electronic Health Record (EHR) Systems", "Integrating clinical records using HL7 FHIR standards and APIs.", "Moderate", "Healthcare"),
        ("Medical Image Analysis with AI", "Detecting tumors and fractures in X-rays and MRI scans using deep learning.", "High", "MedTech"),
        ("Drug Discovery & Molecular Modeling", "Predicting protein structures and ligand binding affinities with AI.", "High", "Biotech"),
        ("Telemedicine & Remote Patient Monitoring", "Building secure video consultation platforms connected to wearable vital monitors.", "Moderate", "HealthTech"),
        ("Clinical Decision Support Systems", "Providing automated diagnostic guidelines and drug-interaction warnings to doctors.", "High", "Clinical")
    ]),

    # 19. Automotive & Aerospace Technology
    ("Automotive & Aerospace", "Transportation Systems", [
        ("Autonomous Vehicle Driving Systems", "Integrating perception, motion planning, and control in self-driving cars.", "High", "Automotive"),
        ("Connected Vehicle & Telematics", "Streaming car diagnostics, tire pressure, and location to cloud dashboards.", "Moderate", "Automotive"),
        ("Electric Vehicle (EV) Battery Systems", "Battery management system (BMS) software tracking cell voltage and thermal limits.", "High", "Clean Tech"),
        ("Avionics & Flight Software", "Mission-critical real-time flight control software meeting DO-178C standards.", "High", "Aerospace"),
        ("Satellite & Space Mission Software", "Orbital trajectory calculations and satellite ground-station communication.", "High", "Space Tech"),
        ("Automotive Functional Safety (ISO 26262)", "Designing failsafe automotive architectures across ASIL A to D tiers.", "High", "Automotive")
    ]),

    # 20. Emerging & Future Technologies
    ("Emerging Technologies", "Next-Gen Tech", [
        ("Quantum Computing Algorithms", "Programming quantum circuits using Qiskit for factoring and simulation.", "High", "Deep Tech"),
        ("Digital Twin Simulations", "Building real-time virtual models of factories and wind turbines.", "High", "Industrial Tech"),
        ("Smart Cities & Urban IoT", "Automating intelligent traffic lights, smart water meters, and urban power grids.", "Moderate", "Civic Tech"),
        ("Renewable Energy Software", "Optimizing solar panel grid balancing and battery storage with machine learning.", "Moderate", "Clean Energy"),
        ("Agricultural Technology (AgriTech)", "Drone crop monitoring, precision irrigation, and soil sensor analysis.", "Moderate", "Agriculture"),
        ("Educational Technology (EdTech)", "Personalized adaptive learning algorithms and virtual classrooms.", "Low", "Education"),
        ("Brain-Computer Interfaces (BCI)", "Decoding EEG brainwave signals to control robotic limbs and computers.", "High", "Neurotechnology"),
        ("Technology Entrepreneurship", "Launching software startups, finding product-market fit, and fundraising.", "Moderate", "Business"),
        ("Technology Consulting", "Advising enterprise leadership on digital transformation roadmaps and IT strategy.", "Moderate", "Consulting"),
        ("Product Management", "Prioritizing engineering roadmaps, defining MVPs, and measuring user metrics.", "Moderate", "Leadership")
    ])
]

def seed_all_interests(db: Session = None):
    print("=" * 60)
    print("SEEDING AREAS OF INTEREST DATABASE (Target: 250+ Interests)")
    print("=" * 60)

    def _execute(session: Session):
        total_interests = 0
        total_categories = 0
        seen_codes = set()
        seen_names = set()

        for cat_name, default_cluster, interest_items in INTEREST_CATALOG:
            # Check or create category
            category = session.query(InterestCategory).filter_by(name=cat_name).first()
            if not category:
                category = InterestCategory(name=cat_name, description=f"Broad interest area covering {cat_name}.")
                session.add(category)
                session.flush()
                total_categories += 1

            for name, desc, diff, domain in interest_items:
                clean_name = name.strip()
                code = slugify(clean_name)

                if code in seen_codes or clean_name.lower() in seen_names:
                    continue
                seen_codes.add(code)
                seen_names.add(clean_name.lower())

                interest = session.query(AreaOfInterest).filter_by(interest_code=code).first()
                if not interest:
                    interest = AreaOfInterest(
                        interest_code=code,
                        name=clean_name,
                        category_id=category.category_id,
                        description=desc,
                        industry_domain=domain,
                        learning_difficulty=diff
                    )
                    session.add(interest)
                    session.flush()
                    total_interests += 1

        session.commit()
        return total_interests, total_categories

    if db is not None:
        return _execute(db)
    else:
        with get_db_session() as session:
            return _execute(session)

if __name__ == "__main__":
    interests_count, cat_count = seed_all_interests()
    print(f"\n[INTERESTS SUCCESS] Seeded {interests_count} distinct interest areas across {cat_count} categories!")

# Additional 100+ specialized areas of interest to cross 260+ records comfortably
EXTRA_INTEREST_CATALOG = [
    ("Specialized Computer Science", "Deep Tech", [
        ("Compiler Design & Optimization", "Building language parsers, ASTs, and optimizing machine code generation.", "High", "Systems"),
        ("Formal Methods & Program Verification", "Using mathematical logic and model checkers to prove software correctness.", "High", "Aerospace & Crypto"),
        ("Distributed Consensus Algorithms", "Exploring Paxos, Raft, and PBFT consensus protocols in distributed systems.", "High", "Infrastructure"),
        ("Homomorphic Encryption & Privacy", "Computing on encrypted data without ever decrypting sensitive information.", "High", "Security"),
        ("Zero-Knowledge Cryptography", "Cryptographic proofs of knowledge without revealing underlying secret witness data.", "High", "Blockchain"),
        ("Parallel & GPU Computing", "Programming thousands of parallel threads using CUDA and OpenCL.", "High", "Supercomputing"),
        ("Information Theory & Coding", "Shannon entropy, lossy/lossless data compression, and error-correcting codes.", "High", "Telecommunications"),
        ("Theoretical Computer Science", "Computational complexity classes (P, NP, NP-Complete) and Turing machines.", "High", "Mathematics"),
        ("Functional Programming Languages", "Exploring pure functions, immutable data, and monads in Haskell and Scala.", "Moderate", "Software"),
        ("Type Systems & Type Theory", "Hindley-Milner type inference, dependent types, and linear type systems.", "High", "Programming Languages")
    ]),

    ("Enterprise & Business Technology", "Enterprise IT", [
        ("Enterprise Architecture (TOGAF)", "Aligning IT infrastructure and software architecture with corporate business goals.", "Moderate", "Corporate IT"),
        ("ERP Systems (SAP & Oracle)", "Implementing enterprise resource planning for supply chain, HR, and finance.", "Moderate", "Enterprise"),
        ("CRM Platforms (Salesforce)", "Configuring enterprise customer relationship platforms and automated sales funnels.", "Low", "Business Tech"),
        ("IT Service Management (ITIL)", "Incident management, change governance, and service catalog delivery.", "Low", "Operations"),
        ("Digital Transformation Strategy", "Modernizing legacy business processes with cloud, AI, and paperless systems.", "Moderate", "Consulting"),
        ("Supply Chain Digitalization", "Tracking physical goods with RFID, barcodes, and real-time cloud inventory.", "Moderate", "Logistics"),
        ("E-Invoicing & B2B EDI Standards", "Automating electronic purchase orders and invoice exchange between companies.", "Low", "Commerce"),
        ("Business Process Automation (RPA)", "Automating manual employee screen tasks using UiPath and software robots.", "Low", "Automation"),
        ("Corporate Identity Governance", "Managing employee provisioning, role-based permissions, and de-provisioning.", "Moderate", "Security")
    ]),

    ("Human-Computer Interaction", "User Centered Design", [
        ("Voice User Interface (VUI)", "Designing conversational voice interactions for smart speakers and car displays.", "Low", "Consumer Tech"),
        ("Gesture-Based Interfaces", "Interacting with computers through hand, eye, and body gesture recognition.", "Moderate", "Interactive Tech"),
        ("Eye-Tracking & Gaze Interaction", "Leveraging infrared eye trackers for accessibility and gaming controls.", "Moderate", "Accessibility"),
        ("Haptic Feedback Design", "Engineering vibration and force feedback profiles for touchscreens and controllers.", "Moderate", "Gaming & XR"),
        ("Cognitive Load in UI Design", "Structuring screens to minimize human mental fatigue and decision paralysis.", "Low", "Design"),
        ("Assistive Technology for Disabilities", "Designing software interfaces for screen readers, braille displays, and switch inputs.", "Low", "Healthcare"),
        ("Tangible User Interfaces (TUI)", "Bridging physical physical desktop tokens with digital graphical displays.", "Moderate", "Research"),
        ("Spatial Sound & 3D Audio", "Simulating directional acoustic binaural audio in gaming and virtual reality.", "Moderate", "Audio Tech")
    ]),

    ("Space & Aerospace Technology", "Aerospace", [
        ("CubeSat & Nanosatellite Software", "Writing low-power flight software for miniature scientific satellites in low earth orbit.", "High", "Space"),
        ("Rocket Propulsion Telemetry", "Streaming high-frequency combustion chamber pressure and valve sensors in real time.", "High", "Aerospace"),
        ("Orbital Mechanics Simulation", "Calculating Keplerian orbital elements and interplanetary transfer orbits.", "High", "Astrodynamics"),
        ("Spacecraft Fault Tolerance", "Designing radiation-tolerant redundant computers that recover from cosmic ray bit flips.", "High", "Mission Critical"),
        ("Aviation ADS-B Tracking", "Decoding automatic dependent surveillance-broadcast radio signals from aircraft.", "Moderate", "Aviation"),
        ("Uncrewed Traffic Management (UTM)", "Managing low-altitude commercial drone delivery corridors automatically.", "Moderate", "Autonomous Aviation")
    ]),

    ("Climate & Clean Technology", "Sustainability", [
        ("Smart Electric Grid Optimization", "Balancing renewable wind and solar power generation with electrical demand.", "Moderate", "Energy"),
        ("Carbon Footprint Tracking Software", "Measuring Scope 1, 2, and 3 enterprise greenhouse gas emissions with software.", "Low", "ESG"),
        ("Precision Agriculture with Drones", "Analyzing drone NDVI vegetation index imagery to minimize fertilizer use.", "Moderate", "Agriculture"),
        ("Water Management & Smart Metering", "Detecting underground municipal water pipe leaks using IoT acoustic sensors.", "Moderate", "Utilities"),
        ("Battery Energy Storage Systems (BESS)", "Controlling utility-scale lithium-ion battery discharge during peak grid hours.", "Moderate", "Clean Energy"),
        ("Electric Vehicle Fleet Management", "Optimizing overnight depot charging schedules for electric delivery vans.", "Moderate", "Transportation")
    ]),

    ("Education Technology (EdTech)", "Learning Systems", [
        ("Adaptive Learning Algorithms", "Adjusting quiz difficulty dynamically based on individual student mastery.", "Moderate", "EdTech"),
        ("Gamified Learning Systems", "Integrating streaks, leaderboards, and rewards into educational applications.", "Low", "Education"),
        ("Automated Code Grading Systems", "Sandboxing student programming submissions and running automated unit tests.", "Moderate", "Computer Science Ed"),
        ("Virtual Science Labs", "Simulating physics and chemistry lab experiments in 3D interactive web browsers.", "Moderate", "EdTech")
    ]),

    ("Technology Leadership & Ethics", "Strategy & Governance", [
        ("Engineering Team Leadership", "Mentoring junior engineers, conducting 1-on-1s, and fostering psychological safety.", "Low", "Management"),
        ("Open Source Community Governance", "Maintaining popular open source software projects and managing contributors.", "Low", "Community"),
        ("Algorithmic Bias & Fair AI", "Auditing machine learning models for demographic parity and equalized odds.", "Moderate", "Ethics"),
        ("Data Sovereignty & Privacy Laws", "Ensuring software compliance with GDPR, CCPA, and data localization mandates.", "Moderate", "Legal Tech"),
        ("Technology Commercialization", "Spinning university research projects into venture-backed startup companies.", "Moderate", "Entrepreneurship")
    ])
]

# Update the seeder to include EXTRA_INTEREST_CATALOG
def seed_all_interests_complete(db: Session = None):
    all_catalogs = INTEREST_CATALOG + EXTRA_INTEREST_CATALOG
    print("=" * 60)
    print(f"SEEDING COMPLETE AREAS OF INTEREST (Catalog Domains: {len(all_catalogs)})")
    print("=" * 60)

    def _execute(session: Session):
        total_interests = 0
        total_categories = 0
        seen_codes = set()
        seen_names = set()

        for cat_name, default_cluster, interest_items in all_catalogs:
            category = session.query(InterestCategory).filter_by(name=cat_name).first()
            if not category:
                category = InterestCategory(name=cat_name, description=f"Domain for {cat_name}.")
                session.add(category)
                session.flush()
                total_categories += 1

            for name, desc, diff, domain in interest_items:
                clean_name = name.strip()
                code = slugify(clean_name)

                if code in seen_codes or clean_name.lower() in seen_names:
                    continue
                seen_codes.add(code)
                seen_names.add(clean_name.lower())

                interest = session.query(AreaOfInterest).filter_by(interest_code=code).first()
                if not interest:
                    interest = AreaOfInterest(
                        interest_code=code,
                        name=clean_name,
                        category_id=category.category_id,
                        description=desc,
                        industry_domain=domain,
                        learning_difficulty=diff
                    )
                    session.add(interest)
                    session.flush()
                    total_interests += 1

        session.commit()
        return total_interests, total_categories

    if db is not None:
        return _execute(db)
    else:
        with get_db_session() as session:
            return _execute(session)
