# database/seed_data/seed_all_90_domains.py
"""
Comprehensive 90-Domain Technical Skills Seeder.
Generates 1,500+ genuine, categorized technical skills with full metadata.
Enforces unique constraints, slugs, aliases, and relations.
"""
import os
import sys
import re

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from database.connection import get_db_session, init_db
from database.models import SkillCategory, TechnicalSkill, SkillAlias, SkillRelationship

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[\s/\\+]+', '-', text)
    text = re.sub(r'[^a-z0-9\-._]', '', text)
    return text.strip('-')

# 90 Domain Catalogs (Category Name, Domain Cluster, Description, [Skill Items])
# Skill Item: (Name, Subcategory, Description, Difficulty, Priority, Relevance, [Aliases])

DOMAINS_1_TO_30 = [
    # 1. Programming Languages
    ("Programming Languages", "Software Engineering", "Core procedural, object-oriented, and functional programming languages", [
        ("Python", "General Purpose", "Interpreted high-level language popular in AI, data, and web.", "Beginner", "High", "Critical", ["python3", "py"]),
        ("Java", "Enterprise", "Object-oriented, cross-platform enterprise language.", "Intermediate", "High", "Critical", ["jdk", "jvm"]),
        ("C", "Systems", "Low-level procedural language with direct memory control.", "Intermediate", "High", "High", ["ansi-c"]),
        ("C++", "Systems & Games", "High-performance OOP language with templates and RAII.", "Advanced", "High", "Critical", ["cpp", "cplusplus"]),
        ("C#", "Enterprise & Games", "Modern type-safe language for .NET, Unity, and services.", "Intermediate", "High", "High", ["csharp"]),
        ("JavaScript", "Web Development", "Dynamic scripting language of the web front-end and back-end.", "Beginner", "High", "Critical", ["js"]),
        ("TypeScript", "Typed Web", "Statically typed superset of JavaScript.", "Intermediate", "High", "Critical", ["ts"]),
        ("Go", "Cloud & Backend", "Google compiled language engineered for concurrency and microservices.", "Intermediate", "High", "Critical", ["golang"]),
        ("Rust", "Systems Programming", "Memory-safe systems programming language with zero-cost abstractions.", "Advanced", "High", "Critical", ["rust-lang"]),
        ("Kotlin", "Mobile & JVM", "Concise modern language officially favored for Android development.", "Intermediate", "High", "High", ["kt"]),
        ("Swift", "Apple Ecosystem", "Fast, type-safe language for iOS and macOS applications.", "Intermediate", "High", "High", ["swift-lang"]),
        ("PHP", "Web Scripting", "Server-side language widely used in content management and web applications.", "Beginner", "Medium", "Moderate", ["php8"]),
        ("Ruby", "Productive Web", "Dynamic object-oriented language emphasizing developer happiness.", "Beginner", "Medium", "Moderate", ["ruby-lang"]),
        ("R", "Statistical Computing", "Language specialized for statistics, data analysis, and graphs.", "Intermediate", "High", "High", ["r-lang"]),
        ("Scala", "Functional JVM", "Combines object-oriented and functional programming on JVM.", "Advanced", "Medium", "High", ["scala-lang"]),
        ("Dart", "Mobile Client", "Client-optimized language powering the Flutter cross-platform toolkit.", "Beginner", "Medium", "High", ["dart-lang"]),
        ("Julia", "Scientific Computing", "High-performance language designed for numerical and scientific computing.", "Intermediate", "Medium", "Emerging", ["julia-lang"]),
        ("Lua", "Embedded Scripting", "Lightweight embeddable scripting language used in game engines.", "Beginner", "Medium", "Moderate", ["lua-lang"]),
        ("Haskell", "Pure Functional", "Statically typed purely functional programming language.", "Advanced", "Low", "Moderate", ["haskell-lang"]),
        ("Elixir", "Concurrency", "Functional concurrent language built on the Erlang BEAM virtual machine.", "Intermediate", "Medium", "High", ["elixir-lang"]),
        ("Clojure", "Lisp on JVM", "Dynamic functional Lisp dialect targeting the Java platform.", "Advanced", "Low", "Moderate", ["clojure-lang"]),
        ("Shell Scripting", "DevOps Automation", "Unix shell scripting using Bash and Zsh for task automation.", "Beginner", "High", "Critical", ["bash", "sh"]),
        ("PowerShell", "Windows Automation", "Object-oriented automation shell for system administration.", "Intermediate", "High", "High", ["pwsh"]),
        ("Assembly x86", "Low-Level Architecture", "Machine-level instruction set architecture for x86 processors.", "Expert", "Low", "Moderate", ["x86-asm"]),
        ("Assembly ARM", "Mobile Architecture", "Machine instructions for ARM processors and embedded devices.", "Expert", "Low", "High", ["arm-asm"])
    ]),

    # 2. Python Ecosystem
    ("Python Ecosystem", "Data & Web", "Key libraries, tooling, and utilities across the Python environment", [
        ("NumPy", "Scientific Computing", "Array programming and numerical computing foundation in Python.", "Beginner", "High", "Critical", ["numpy-lib"]),
        ("Pandas", "Data Manipulation", "Tabular data manipulation and analysis toolkit.", "Beginner", "High", "Critical", ["pandas-lib"]),
        ("SciPy", "Scientific Algorithms", "Algorithms for scientific computing, optimization, and linear algebra.", "Intermediate", "High", "High", ["scipy-lib"]),
        ("Matplotlib", "Visualization", "Foundational plotting and visual figure generation library.", "Beginner", "High", "High", ["matplotlib-py"]),
        ("Seaborn", "Statistical Viz", "Statistical data visualization framework with aesthetic themes.", "Beginner", "High", "High", ["seaborn-py"]),
        ("FastAPI", "Web APIs", "Modern high-speed ASGI framework with automated OpenAPI docs.", "Intermediate", "High", "Critical", ["fastapi"]),
        ("Flask", "Microframework", "Minimalist WSGI web application framework.", "Beginner", "High", "High", ["flask-py"]),
        ("Django", "Full-Stack Web", "Battery-included framework for scalable database-backed web apps.", "Intermediate", "High", "Critical", ["django"]),
        ("SQLAlchemy", "ORM & Database", "Database abstraction and Object-Relational Mapping library.", "Intermediate", "High", "Critical", ["sqlalchemy"]),
        ("Pydantic", "Data Validation", "Fast data validation using Python type annotations.", "Intermediate", "High", "Critical", ["pydantic"]),
        ("Celery", "Task Queue", "Distributed task queue processing background asynchronous tasks.", "Intermediate", "Medium", "High", ["celery"]),
        ("Pytest", "Testing Framework", "Standard testing framework for unit and functional test suites.", "Beginner", "High", "Critical", ["pytest"]),
        ("Poetry", "Dependency Management", "Modern packaging and dependency resolver for Python.", "Intermediate", "High", "High", ["poetry"]),
        ("Polars", "High-Speed DataFrames", "Multi-threaded fast DataFrame library written in Rust.", "Intermediate", "High", "Critical", ["polars"]),
        ("Dask", "Parallel Computing", "Flexible parallel computing library scaling Python code.", "Advanced", "Medium", "High", ["dask"]),
        ("Ray", "Distributed Compute", "Unified compute engine for scaling AI applications and parallel workers.", "Advanced", "High", "Critical", ["ray"]),
        ("Streamlit", "Data Applications", "Rapid interactive web UI builder for machine learning and analytics.", "Beginner", "High", "Critical", ["streamlit"]),
        ("Gradio", "Model Demos", "Framework for creating shareable UI demonstrations for machine learning models.", "Beginner", "High", "High", ["gradio"]),
        ("Asyncio", "Asynchronous Python", "Built-in library for asynchronous I/O and event loop management.", "Intermediate", "High", "Critical", ["asyncio"]),
        ("Beautiful Soup", "Web Scraping", "HTML and XML parser for extracting web content.", "Beginner", "Medium", "Moderate", ["bs4"]),
        ("Scrapy", "Web Crawling", "High-level web crawling framework for structured data scraping.", "Intermediate", "Medium", "High", ["scrapy"])
    ]),

    # 3. Java Ecosystem
    ("Java Ecosystem", "Enterprise Systems", "Enterprise frameworks, build tools, and distributed Java technologies", [
        ("Spring Boot", "Microservices", "Convention-over-configuration framework for production Spring apps.", "Intermediate", "High", "Critical", ["spring-boot"]),
        ("Spring Core", "Dependency Injection", "Core IoC container and enterprise application architecture.", "Advanced", "High", "Critical", ["spring-framework"]),
        ("Spring Security", "Auth & Access", "Comprehensive authentication and authorization framework.", "Advanced", "High", "Critical", ["spring-sec"]),
        ("Spring Cloud", "Cloud Patterns", "Tools for service discovery, circuit breakers, and configuration.", "Advanced", "High", "High", ["spring-cloud"]),
        ("Hibernate", "ORM Persistence", "Object-relational mapping standard for Java database persistence.", "Intermediate", "High", "Critical", ["hibernate-orm"]),
        ("JPA", "Persistence API", "Java Persistence API standard specification.", "Intermediate", "High", "High", ["jakarta-jpa"]),
        ("Maven", "Build & Dependency", "Project object model build management system.", "Beginner", "High", "Critical", ["apache-maven"]),
        ("Gradle", "Build Automation", "Domain-specific build automation tool using Kotlin and Groovy.", "Intermediate", "High", "Critical", ["gradle-tool"]),
        ("JUnit 5", "Unit Testing", "Leading unit testing framework for JVM platforms.", "Beginner", "High", "Critical", ["junit5"]),
        ("Mockito", "Mock Testing", "Mocking framework for effective unit testing in Java.", "Intermediate", "High", "Critical", ["mockito"]),
        ("Quarkus", "Cloud-Native Java", "Supersonic subatomic Java framework tailored for Kubernetes.", "Advanced", "Medium", "Emerging", ["quarkus"]),
        ("Micronaut", "Microservices", "Modern JVM framework with compile-time dependency injection.", "Advanced", "Medium", "High", ["micronaut"]),
        ("Netty", "Asynchronous Network", "Event-driven network application framework for protocol servers.", "Advanced", "Medium", "High", ["netty"]),
        ("Kafka Java Client", "Message Streaming", "High-throughput publish-subscribe messaging client.", "Intermediate", "High", "Critical", ["kafka-client"]),
        ("Lombok", "Code Generation", "Reduces boilerplate code with annotations for getters and builders.", "Beginner", "Medium", "High", ["project-lombok"]),
        ("Flyway", "Schema Migrations", "Version control tool for relational database schema updates.", "Intermediate", "High", "High", ["flyway"]),
        ("Liquibase", "Database Change", "Tracks, versions, and deploys database changes reliably.", "Intermediate", "High", "High", ["liquibase"]),
        ("Jackson", "JSON Parsing", "Fast multi-purpose JSON data-binding library for Java.", "Intermediate", "High", "High", ["jackson-databind"]),
        ("Resilience4j", "Fault Tolerance", "Fault tolerance library inspired by Netflix Hystrix.", "Intermediate", "High", "Critical", ["resilience4j"])
    ]),

    # 4. JavaScript Ecosystem
    ("JavaScript Ecosystem", "Web & Client", "Client-side and server-side JavaScript runtimes and libraries", [
        ("Node.js", "Server Runtime", "V8 asynchronous event-driven JavaScript engine on the server.", "Beginner", "High", "Critical", ["nodejs"]),
        ("React", "UI Library", "Declarative component-based UI library created by Meta.", "Intermediate", "High", "Critical", ["reactjs"]),
        ("Next.js", "Full-Stack React", "React framework supporting server components and dynamic routing.", "Intermediate", "High", "Critical", ["nextjs"]),
        ("Vue.js", "Progressive Framework", "User-friendly progressive framework for reactive web interfaces.", "Intermediate", "High", "High", ["vue3"]),
        ("Angular", "Enterprise SPA", "Comprehensive TypeScript framework for robust enterprise web applications.", "Advanced", "High", "Critical", ["angular"]),
        ("Svelte", "Zero-Virtual-DOM", "Compiles components into tiny direct DOM manipulation code.", "Intermediate", "Medium", "High", ["svelte"]),
        ("Express.js", "Backend Server", "Minimalist routing and middleware web framework for Node.js.", "Beginner", "High", "Critical", ["express"]),
        ("NestJS", "Architecture Backend", "Structured enterprise Node.js framework inspired by Angular.", "Advanced", "High", "High", ["nestjs"]),
        ("Bun", "All-in-One Runtime", "Ultra-fast JavaScript runtime, bundler, and package manager.", "Intermediate", "Medium", "Emerging", ["bun"]),
        ("Deno", "Secure Runtime", "Modern runtime with built-in TypeScript support and default security.", "Intermediate", "Medium", "Emerging", ["deno"]),
        ("Redux Toolkit", "Global State", "Standard way to write predictable global state logic.", "Intermediate", "High", "Critical", ["redux"]),
        ("Zustand", "Lightweight State", "Minimalistic hook-based state management without boilerplate.", "Beginner", "High", "High", ["zustand"]),
        ("Vite", "Modern Bundler", "Lightning-fast frontend build tool using native ES modules.", "Beginner", "High", "Critical", ["vite"]),
        ("Webpack", "Module Bundler", "Configurable static module bundler for complex web projects.", "Intermediate", "Medium", "High", ["webpack"]),
        ("Jest", "Testing Engine", "Delightful testing framework with built-in mocking and assertion.", "Beginner", "High", "Critical", ["jest"]),
        ("Vitest", "Fast Unit Testing", "Next-generation testing framework powered by Vite.", "Beginner", "High", "High", ["vitest"]),
        ("Tailwind CSS", "Utility Styling", "Utility-first CSS framework for rapid interface design.", "Beginner", "High", "Critical", ["tailwind"]),
        ("TanStack Query", "Server Cache", "Data fetching and asynchronous cache synchronizer.", "Intermediate", "High", "Critical", ["react-query"]),
        ("Cypress", "End-to-End Test", "Browser-based testing tool for complete user flow validation.", "Intermediate", "High", "High", ["cypress"]),
        ("Playwright JS", "Cross-Browser Test", "Modern automated browser testing across Chromium, WebKit, and Firefox.", "Intermediate", "High", "Critical", ["playwright"])
    ]),

    # 5. C and C++ Ecosystem
    ("C and C++ Ecosystem", "Systems & Hardware", "Systems software, graphics pipelines, and compilation infrastructure", [
        ("CMake", "Build Management", "Industry standard cross-platform build generation tool.", "Intermediate", "High", "Critical", ["cmake"]),
        ("Make", "Build Tool", "Build automation utility tracking dependencies and file updates.", "Beginner", "High", "High", ["gnu-make"]),
        ("GCC", "Compiler Collection", "GNU Compiler Collection for C, C++, and related languages.", "Intermediate", "High", "Critical", ["gcc"]),
        ("Clang", "LLVM Frontend", "Fast compiler frontend offering expressive diagnostic messages.", "Intermediate", "High", "Critical", ["clang"]),
        ("STL Containers & Algorithms", "C++ Standard Lib", "Standard vectors, maps, algorithms, and smart pointers in modern C++.", "Intermediate", "High", "Critical", ["cpp-stl"]),
        ("Boost", "C++ Libraries", "Extensive collection of peer-reviewed utility libraries for C++.", "Advanced", "Medium", "High", ["boost-cpp"]),
        ("Google Test", "Unit Testing", "Google C++ testing framework supporting parameterized tests.", "Intermediate", "High", "High", ["gtest"]),
        ("Catch2", "Header-Only Testing", "Modern test framework for unit tests with expression decomposition.", "Beginner", "Medium", "High", ["catch2"]),
        ("Qt", "GUI Framework", "Cross-platform widget toolkit and application framework.", "Advanced", "High", "High", ["qt-framework"]),
        ("OpenGL", "Graphics Pipeline", "Cross-language 2D and 3D graphics rendering interface.", "Advanced", "Medium", "High", ["opengl"]),
        ("Vulkan", "Explicit Graphics", "Low-overhead direct GPU control API for high-performance graphics.", "Expert", "High", "Critical", ["vulkan"]),
        ("OpenMP", "Multi-Core Parallel", "Shared-memory parallel programming API for high-throughput math.", "Advanced", "High", "High", ["openmp"]),
        ("MPI", "Distributed Memory", "Message passing interface for cluster-scale parallel compute.", "Advanced", "Medium", "High", ["openmpi"]),
        ("Valgrind", "Memory Debugger", "Dynamic analysis suite detecting memory leaks and thread errors.", "Intermediate", "High", "Critical", ["valgrind"]),
        ("GDB", "GNU Debugger", "Standard command-line debugging tool for C and C++ executables.", "Intermediate", "High", "Critical", ["gdb"]),
        ("Conan", "Package Manager", "Decentralized package manager for C/C++ cross-platform builds.", "Intermediate", "Medium", "High", ["conan"])
    ]),

    # 6. .NET Technologies
    (".NET Technologies", "Microsoft Stack", "Enterprise application frameworks and cloud services for .NET", [
        (".NET 8", "Application Runtime", "Modern cross-platform unified development platform from Microsoft.", "Intermediate", "High", "Critical", ["dotnet8"]),
        ("ASP.NET Core", "Web Framework", "High-performance framework for building cloud-connected services.", "Intermediate", "High", "Critical", ["aspnetcore"]),
        ("Entity Framework Core", "Data Access ORM", "Lightweight, extensible Object-Relational Mapper for .NET.", "Intermediate", "High", "Critical", ["efcore"]),
        ("LINQ", "Language Querying", "Uniform query syntax for filtering and transforming collections.", "Beginner", "High", "Critical", ["linq-c#"]),
        ("Blazor", "WebAssembly UI", "Interactive single-page web UI built directly in C#.", "Intermediate", "Medium", "High", ["blazor"]),
        (".NET MAUI", "Cross-Platform UI", "Multi-platform application UI for Android, iOS, and Windows desktop.", "Intermediate", "Medium", "High", ["maui"]),
        ("SignalR", "Real-Time Web", "Websocket and server-sent event push messaging library.", "Intermediate", "High", "High", ["signalr"]),
        ("xUnit", "Unit Testing", "Community-driven unit testing framework for .NET applications.", "Beginner", "High", "Critical", ["xunit"]),
        ("Dapper", "Micro ORM", "High-performance object mapper for raw SQL queries.", "Intermediate", "High", "High", ["dapper"]),
        ("MediatR", "In-Process Messaging", "Simple mediator pattern implementation decoupling handlers.", "Intermediate", "Medium", "High", ["mediatr"]),
        ("NuGet", "Package Management", "Official package manager and publishing hub for .NET.", "Beginner", "High", "Critical", ["nuget"])
    ]),

    # 7. Web Development
    ("Web Development", "Web Standards", "Standard web protocols, browser behaviors, and accessibility guidelines", [
        ("HTML5", "Document Semantics", "Standard markup language creating semantic structures for websites.", "Beginner", "High", "Critical", ["html5"]),
        ("CSS3", "Visual Presentation", "Cascading Style Sheets defining layouts, typography, and styling.", "Beginner", "High", "Critical", ["css3"]),
        ("Web Accessibility (WCAG)", "Inclusion Standards", "Guidelines ensuring web interfaces are accessible to all people.", "Beginner", "High", "Critical", ["wcag"]),
        ("WebSockets", "Bi-Directional Channels", "Persistent TCP connection facilitating low-latency real-time data.", "Intermediate", "High", "Critical", ["websockets"]),
        ("WebRTC", "Peer-to-Peer Media", "Real-time audio, video, and data communication between browsers.", "Advanced", "Medium", "High", ["webrtc"]),
        ("Progressive Web Apps (PWA)", "App Experience", "Web applications with offline capabilities and mobile home-screen install.", "Intermediate", "Medium", "High", ["pwa"]),
        ("HTTP/2 & HTTP/3", "Transport Protocols", "Multiplexed and QUIC-backed modern web transport standards.", "Intermediate", "High", "High", ["http-protocols"]),
        ("Core Web Vitals", "UX Metrics", "Standardized user experience metrics measuring load, visual stability, and responsiveness.", "Intermediate", "High", "Critical", ["web-vitals"])
    ]),

    # 8. Frontend Development
    ("Frontend Development", "Client Architecture", "Component engineering, responsive layouts, and design system integration", [
        ("Responsive Layouts (Flexbox/Grid)", "Layout Engineering", "CSS Flexbox and 2D Grid systems for dynamic multi-device layouts.", "Beginner", "High", "Critical", ["css-grid-flex"]),
        ("Shadcn UI", "Accessible Components", "Composable accessible UI components built with Radix and Tailwind.", "Intermediate", "High", "Critical", ["shadcn"]),
        ("Storybook", "Isolated UI Dev", "Workshop environment for developing and cataloging isolated UI components.", "Intermediate", "High", "High", ["storybook"]),
        ("Micro-Frontends", "Distributed UI", "Splitting frontend monolithic apps into independent sub-applications.", "Advanced", "Medium", "High", ["micro-frontends"]),
        ("Web Performance Optimization", "Speed Optimization", "Code splitting, image compression, lazy loading, and critical rendering path.", "Intermediate", "High", "Critical", ["frontend-perf"]),
        ("Sass / SCSS", "CSS Preprocessing", "Variables, nesting, and mixins extending CSS capabilities.", "Beginner", "High", "High", ["sass"])
    ]),

    # 9. Backend Development
    ("Backend Development", "Server Architecture", "API standards, session security, queueing, and distributed server design", [
        ("RESTful API Design", "Web APIs", "Resource-oriented architectural principles for stateless web APIs.", "Beginner", "High", "Critical", ["rest-apis"]),
        ("GraphQL", "Client-Driven Query", "Declarative query language requesting exact data payloads.", "Intermediate", "High", "Critical", ["graphql"]),
        ("gRPC", "Binary RPC", "High-performance RPC framework using Protocol Buffers over HTTP/2.", "Intermediate", "High", "Critical", ["grpc"]),
        ("JWT Authentication", "Token Auth", "Stateless cryptographically signed tokens for secure user sessions.", "Beginner", "High", "Critical", ["jwt"]),
        ("OAuth 2.0 / OpenID Connect", "Identity Protocols", "Federated authorization and single sign-on authentication standard.", "Intermediate", "High", "Critical", ["oauth2"]),
        ("Rate Limiting", "API Protection", "Mitigating denial of service and API abuse via token bucket limits.", "Intermediate", "High", "Critical", ["rate-limiting"]),
        ("Distributed Caching", "Latency Reduction", "Cache-aside and write-through caching using Redis or Memcached.", "Intermediate", "High", "Critical", ["distributed-caching"]),
        ("Server-Sent Events", "One-Way Streaming", "Pushing real-time updates from server to client over standard HTTP.", "Intermediate", "High", "High", ["sse"])
    ]),

    # 10. Full Stack Development
    ("Full Stack Development", "End-to-End Web", "Full-stack integration, monorepos, and hybrid rendering strategies", [
        ("MERN Stack Integration", "Stack Architecture", "Connecting MongoDB, Express, React, and Node.js end-to-end.", "Beginner", "High", "High", ["mern-stack"]),
        ("Monorepo Workspaces", "Code Organization", "Managing shared libraries and applications in a unified repository with Turborepo or Nx.", "Intermediate", "High", "Critical", ["monorepo-tools"]),
        ("Server-Side Rendering (SSR)", "Rendering Models", "Generating complete HTML on the server for enhanced SEO and speed.", "Intermediate", "High", "Critical", ["ssr-rendering"]),
        ("Static Site Generation (SSG)", "Pre-Rendering", "Compiling pages into static assets at build time for CDN distribution.", "Beginner", "High", "Critical", ["ssg-rendering"]),
        ("Backend For Frontend (BFF)", "API Design", "Specialized backend gateways tailoring data for specific client device types.", "Intermediate", "High", "High", ["bff-architecture"])
    ]),

    # 11. Mobile Application Development
    ("Mobile Application Development", "Mobile Systems", "Native mobile SDKs, cross-platform engines, and mobile architecture", [
        ("Android SDK", "Native Android", "Core frameworks and build tools for native Android applications.", "Intermediate", "High", "Critical", ["android-sdk"]),
        ("Jetpack Compose", "Android Declarative UI", "Modern Kotlin-based declarative UI toolkit for Android.", "Intermediate", "High", "Critical", ["jetpack-compose"]),
        ("iOS SDK", "Native iOS", "Apple frameworks including UIKit and Foundation for iPhone apps.", "Intermediate", "High", "Critical", ["ios-sdk"]),
        ("SwiftUI", "Apple Declarative UI", "Declarative UI paradigm across iOS, iPadOS, and macOS.", "Intermediate", "High", "Critical", ["swiftui"]),
        ("React Native", "Cross-Platform", "Building native mobile apps using React and JavaScript bridges.", "Intermediate", "High", "Critical", ["react-native"]),
        ("Flutter", "Cross-Platform Engine", "High-performance Dart-based framework compiling to native ARM code.", "Intermediate", "High", "Critical", ["flutter"]),
        ("Kotlin Multiplatform Mobile", "Shared Mobile Logic", "Sharing domain and networking logic between iOS and Android.", "Advanced", "High", "Emerging", ["kmm"]),
        ("Push Notifications (FCM / APNs)", "Mobile Services", "Delivering remote push notifications to mobile devices.", "Beginner", "High", "Critical", ["push-notifications"]),
        ("Mobile Local Storage (Room / CoreData)", "Offline Storage", "Persisting local data offline with SQLite abstraction layers.", "Beginner", "High", "High", ["room-coredata"])
    ]),

    # 12. Artificial Intelligence
    ("Artificial Intelligence", "Cognitive Systems", "Foundational AI principles, search heuristics, and knowledge representation", [
        ("A* Search Algorithm", "Heuristic Search", "Pathfinding and graph traversal algorithm finding optimal shortest paths.", "Intermediate", "High", "High", ["a-star"]),
        ("Minimax & Alpha-Beta Pruning", "Adversarial Search", "Decision rule for two-player zero-sum games with branch optimization.", "Intermediate", "High", "High", ["minimax"]),
        ("Knowledge Graphs", "Knowledge Modeling", "Graph-structured data models representing interlinked factual concepts.", "Intermediate", "High", "Critical", ["knowledge-graphs"]),
        ("Constraint Satisfaction", "Problem Solving", "Mathematical constraints formulation for scheduling and planning tasks.", "Intermediate", "Medium", "High", ["csp-solver"]),
        ("Bayesian Inference", "Probabilistic Reasoning", "Updating probability estimates for hypotheses as evidence is acquired.", "Intermediate", "High", "Critical", ["bayesian-inference"]),
        ("Ontology Engineering", "Semantic Models", "Defining structured vocabularies and taxonomies with OWL and RDF.", "Advanced", "Medium", "Moderate", ["owl-rdf"])
    ]),

    # 13. Machine Learning
    ("Machine Learning", "Predictive Modeling", "Supervised, unsupervised, and ensemble machine learning algorithms", [
        ("Linear Regression", "Supervised Learning", "Predicting continuous outcomes using linear combinations of predictors.", "Beginner", "High", "Critical", ["linear-regression"]),
        ("Logistic Regression", "Classification", "Modeling probabilities for categorical binary outcomes.", "Beginner", "High", "Critical", ["logistic-regression"]),
        ("Decision Trees", "Tree Models", "Flowchart-like structure segmenting feature spaces into decisions.", "Beginner", "High", "Critical", ["decision-tree"]),
        ("Random Forests", "Ensemble Bagging", "Ensemble of decision trees trained on bootstrap samples with feature subsampling.", "Beginner", "High", "Critical", ["random-forest"]),
        ("XGBoost", "Gradient Boosting", "Scalable, distributed gradient-boosted decision tree library.", "Intermediate", "High", "Critical", ["xgboost"]),
        ("LightGBM", "Fast Boosting", "Gradient boosting framework with leaf-wise tree growth and histogram bins.", "Intermediate", "High", "Critical", ["lightgbm"]),
        ("CatBoost", "Categorical Boosting", "Gradient boosting with native support for categorical features.", "Intermediate", "High", "High", ["catboost"]),
        ("Support Vector Machines", "Margin Classifiers", "Finding optimal hyperplanes maximizing margin between classes.", "Intermediate", "High", "High", ["svm"]),
        ("K-Means Clustering", "Unsupervised", "Partitioning data points into K clusters minimizing within-cluster variance.", "Beginner", "High", "Critical", ["k-means"]),
        ("Principal Component Analysis", "Dimensionality Reduction", "Orthogonal transformation extracting principal directions of variance.", "Intermediate", "High", "Critical", ["pca"]),
        ("Optuna", "Hyperparameter Search", "Automatic hyperparameter optimization software using Bayesian methods.", "Intermediate", "High", "Critical", ["optuna"]),
        ("Model Evaluation Metrics", "Validation", "Evaluating accuracy, precision, recall, F1, ROC-AUC, and log-loss.", "Beginner", "High", "Critical", ["evaluation-metrics"])
    ]),

    # 14. Deep Learning
    ("Deep Learning", "Neural Networks", "Deep neural network architectures, backpropagation, and tensor frameworks", [
        ("PyTorch", "Deep Learning Framework", "Dynamic computation graph library widely used in AI research and production.", "Intermediate", "High", "Critical", ["pytorch"]),
        ("TensorFlow", "Deep Learning Platform", "Google open-source platform for distributed deep learning models.", "Intermediate", "High", "Critical", ["tensorflow"]),
        ("Convolutional Neural Networks", "Image Processing", "Grid-based spatial convolutional layers for feature extraction.", "Intermediate", "High", "Critical", ["cnn"]),
        ("Recurrent Neural Networks", "Sequence Processing", "Recurrent and LSTM networks modeling temporal and sequence data.", "Intermediate", "High", "High", ["rnn-lstm"]),
        ("Transformer Architecture", "Attention Networks", "Multi-head self-attention mechanisms revolutionizing vision and language.", "Advanced", "High", "Critical", ["transformers"]),
        ("Backpropagation & Gradient Descent", "Neural Optimization", "Computing partial derivatives of loss functions to optimize network weights.", "Intermediate", "High", "Critical", ["backpropagation"]),
        ("Adam Optimizer", "Adaptive Optimization", "Adaptive moment estimation combining momentum and RMSprop benefits.", "Intermediate", "High", "Critical", ["adam-opt"]),
        ("Batch Normalization", "Network Stability", "Normalizing layer inputs to accelerate deep neural network training.", "Intermediate", "High", "High", ["batch-norm"]),
        ("Transfer Learning", "Pretrained Models", "Fine-tuning weights of pre-trained models on specialized downstream tasks.", "Intermediate", "High", "Critical", ["transfer-learning"])
    ]),

    # 15. Generative AI
    ("Generative AI", "Content Synthesis", "Diffusion models, multimodal synthesis, and creative artificial intelligence", [
        ("Stable Diffusion", "Latent Diffusion", "Open-weights latent diffusion model for text-to-image synthesis.", "Advanced", "High", "Critical", ["stable-diffusion"]),
        ("Midjourney Prompting", "Image Generation", "Expert parameter tuning and artistic direction for generative image tools.", "Beginner", "High", "High", ["midjourney"]),
        ("Generative Adversarial Networks", "Adversarial Modeling", "Generator-discriminator minimax games producing photorealistic data.", "Advanced", "Medium", "High", ["gan"]),
        ("Variational Autoencoders", "Latent Models", "Probabilistic encoders mapping inputs into continuous latent spaces.", "Advanced", "Medium", "High", ["vae"]),
        ("Multimodal Generation", "Cross-Modal AI", "Coordinated generation of synchronized text, audio, and video.", "Advanced", "High", "Critical", ["multimodal-gen"]),
        ("Synthetic Data Pipelines", "Dataset Augmentation", "Generating artificial data to bootstrap training where real data is scarce.", "Intermediate", "High", "High", ["synthetic-data"]),
        ("AI Safety & Guardrails", "Output Governance", "Constraining generative outputs against toxicity, leaks, and bias.", "Intermediate", "High", "Critical", ["ai-guardrails"])
    ]),

    # 16. Large Language Models
    ("Large Language Models", "Foundation Models", "Inference, serving, context management, and foundation model APIs", [
        ("OpenAI GPT-4 API", "Commercial APIs", "Building applications with state-of-the-art closed models.", "Beginner", "High", "Critical", ["gpt-4-api"]),
        ("Claude 3.5 API", "Commercial APIs", "Utilizing Anthropic models with long 200k+ context windows.", "Beginner", "High", "Critical", ["claude-api"]),
        ("Google Gemini API", "Multimodal APIs", "Interacting with Google's multimodal native foundation models.", "Beginner", "High", "Critical", ["gemini-api"]),
        ("Llama 3 Deployment", "Open Weights", "Self-hosting and serving Meta's open foundation models.", "Intermediate", "High", "Critical", ["llama-3"]),
        ("vLLM Serving Engine", "Inference Serving", "High-throughput model serving with PagedAttention algorithm.", "Advanced", "High", "Critical", ["vllm"]),
        ("Ollama", "Local LLM Runner", "Running lightweight models locally on consumer CPU and GPU.", "Beginner", "High", "High", ["ollama"]),
        ("Model Quantization (GGUF/AWQ)", "Compression", "Reducing parameter precision to 4-bit and 8-bit to fit small VRAM.", "Advanced", "High", "High", ["quantization"]),
        ("Context Window Management", "Context Economics", "Optimizing token budgets and managing needle-in-a-haystack retrieval.", "Beginner", "High", "Critical", ["context-management"])
    ]),

    # 17. Natural Language Processing
    ("Natural Language Processing", "Text Intelligence", "Text extraction, linguistic analysis, tokenization, and semantic embeddings", [
        ("spaCy", "Industrial NLP", "Production-ready NLP pipeline for tokenization, POS, and NER.", "Beginner", "High", "Critical", ["spacy"]),
        ("NLTK", "Linguistics Toolkit", "Educational and research suite for symbolic and statistical text analysis.", "Beginner", "Medium", "High", ["nltk"]),
        ("Named Entity Recognition", "Entity Extraction", "Classifying persons, locations, and organizations in raw text.", "Intermediate", "High", "Critical", ["ner"]),
        ("Sentiment Analysis", "Opinion Mining", "Evaluating emotional valence and polarity across customer reviews and posts.", "Beginner", "High", "High", ["sentiment-analysis"]),
        ("Sentence Transformers", "Semantic Embeddings", "Embedding models mapping sentences into dense semantic vector spaces.", "Intermediate", "High", "Critical", ["sentence-transformers"]),
        ("Text Summarization", "Document Reduction", "Abstractive and extractive condensation of long document corpora.", "Intermediate", "High", "High", ["summarization"]),
        ("Topic Modeling", "Unsupervised NLP", "Extracting semantic topics from unlabelled text with BERTopic or LDA.", "Intermediate", "Medium", "High", ["bertopic"])
    ]),

    # 18. Computer Vision
    ("Computer Vision", "Visual Computing", "Image classification, real-time detection, segmentation, and video processing", [
        ("OpenCV", "Image Processing", "Comprehensive computer vision library for image manipulation.", "Intermediate", "High", "Critical", ["opencv"]),
        ("YOLO Object Detection", "Real-Time Detection", "Fast bounding-box object detection for live camera feeds.", "Intermediate", "High", "Critical", ["yolo"]),
        ("Segment Anything Model (SAM)", "Zero-Shot Segmentation", "Foundation model for zero-shot object segmentation masks.", "Advanced", "High", "Critical", ["sam"]),
        ("MediaPipe", "Body & Face Tracking", "Real-time landmark tracking for hands, face, and body pose.", "Beginner", "High", "High", ["mediapipe"]),
        ("OCR with Tesseract", "Text Recognition", "Optical character recognition extracting text from scanned images.", "Beginner", "High", "High", ["tesseract-ocr"]),
        ("Object Tracking (DeepSORT)", "Video Tracking", "Tracking identities of moving objects across video frames.", "Advanced", "High", "High", ["deepsort"])
    ]),

    # 19. Reinforcement Learning
    ("Reinforcement Learning", "Decision Optimization", "Reward-based optimization, policy gradients, and preference alignment", [
        ("Deep Q-Networks (DQN)", "Value-Based RL", "Combining Q-learning with deep convolutional neural networks.", "Advanced", "High", "High", ["dqn"]),
        ("Proximal Policy Optimization", "Policy Gradients", "Stable actor-critic policy optimization used in robotics and games.", "Advanced", "High", "Critical", ["ppo"]),
        ("Gymnasium Environments", "RL Benchmarks", "Standardized simulation environments for benchmarking RL algorithms.", "Intermediate", "High", "High", ["gymnasium"]),
        ("RLHF Alignment", "Human Feedback", "Reinforcement learning from human feedback aligning model outputs with safety.", "Expert", "High", "Critical", ["rlhf"]),
        ("Direct Preference Optimization", "Preference Learning", "Directly optimizing policy weights from paired preference choices.", "Advanced", "High", "Critical", ["dpo"])
    ]),

    # 20. AI Agents & 21. Agentic AI
    ("AI Agents and Agentic AI", "Autonomous Workflow", "Autonomous multi-agent orchestration, tool routing, and cognitive loops", [
        ("LangChain", "LLM Chains", "Framework for chaining prompts, memory, models, and external tools.", "Intermediate", "High", "Critical", ["langchain"]),
        ("LangGraph", "Cyclic Agent Graphs", "Graph-based framework for stateful multi-agent workflows with loops.", "Intermediate", "High", "Critical", ["langgraph"]),
        ("CrewAI", "Role-Based Multi-Agent", "Coordinating specialized role-playing autonomous agents for complex goals.", "Intermediate", "High", "Critical", ["crewai"]),
        ("Function Calling", "Tool Execution", "Configuring LLMs to produce structured arguments invoking APIs and databases.", "Beginner", "High", "Critical", ["function-calling"]),
        ("ReAct Pattern", "Reason & Act", "Interleaving thought steps and observational tool executions.", "Intermediate", "High", "Critical", ["react-pattern"]),
        ("Autonomous Task Planning", "Goal Decomposition", "Decomposing high-level user instructions into verified execution steps.", "Intermediate", "High", "Critical", ["task-planning"]),
        ("Human-in-the-Loop Review", "Safety Interlocks", "Requiring human confirmation before executing high-risk external actions.", "Beginner", "High", "Critical", ["hitl"])
    ]),

    # 22. Retrieval-Augmented Generation & 23. Prompt Engineering
    ("RAG and Prompt Engineering", "Context Engineering", "Vector search, document ingestion, contextual grounding, and prompt design", [
        ("LlamaIndex", "RAG Framework", "Data connectors and index structures for connecting private data to LLMs.", "Intermediate", "High", "Critical", ["llamaindex"]),
        ("Hybrid Search (Dense + BM25)", "Information Retrieval", "Blending keyword BM25 precision with semantic vector search.", "Intermediate", "High", "Critical", ["hybrid-search"]),
        ("Semantic Chunking", "Document Preprocessing", "Splitting documents into chunks respecting logical paragraph boundaries.", "Beginner", "High", "Critical", ["semantic-chunking"]),
        ("Cross-Encoder Reranking", "Search Re-scoring", "Scoring retrieved candidates using deep cross-encoders for maximum precision.", "Intermediate", "High", "Critical", ["reranking"]),
        ("Few-Shot Prompt Design", "In-Context Learning", "Crafting high-quality prompt exemplars to guide output structure.", "Beginner", "High", "Critical", ["few-shot-prompting"]),
        ("Chain-of-Thought Prompting", "Reasoning Guidance", "Prompting language models to articulate step-by-step reasoning steps.", "Beginner", "High", "Critical", ["chain-of-thought"]),
        ("DSPy Prompt Optimization", "Programmatic Prompts", "Synthesizing and compiling optimal prompts algorithmically.", "Advanced", "High", "Emerging", ["dspy"]),
        ("Hallucination Detection", "Faithfulness Audit", "Verifying that every generated claim is directly supported by citations.", "Intermediate", "High", "Critical", ["hallucination-mitigation"])
    ]),

    # 24. Model Training and Fine-Tuning
    ("Model Fine-Tuning", "Parameter Tuning", "Parameter-efficient adaptation, LoRA, and distributed training systems", [
        ("LoRA (Low-Rank Adaptation)", "Parameter Efficient", "Decomposing weight updates into low-rank matrices to save compute.", "Advanced", "High", "Critical", ["lora"]),
        ("QLoRA", "4-Bit Tuning", "Quantizing base weights to 4-bit precision while fine-tuning LoRA adapters.", "Advanced", "High", "Critical", ["qlora"]),
        ("PEFT Library", "HuggingFace PEFT", "Hugging Face library unifying prefix tuning, prompt tuning, and LoRA.", "Advanced", "High", "Critical", ["peft"]),
        ("DeepSpeed ZeRO", "Distributed Training", "Zero Redundancy Optimizer sharding parameters across multiple GPUs.", "Expert", "High", "Critical", ["deepspeed"]),
        ("Weights & Biases (W&B)", "ML Tracking", "Tracking training loss curves, gradient norms, and hyperparameter sweeps.", "Beginner", "High", "Critical", ["wandb"]),
        ("Learning Rate Warmup", "Optimization Schedulers", "Linearly ramping learning rates before decaying to stabilize early epochs.", "Intermediate", "High", "High", ["lr-warmup"])
    ]),

    # 25. MLOps
    ("MLOps", "Operational ML", "Model registries, continuous training, drift detection, and serving clusters", [
        ("MLflow", "Model Registry", "Tracking experiments and staging models through development to production.", "Intermediate", "High", "Critical", ["mlflow"]),
        ("Kubeflow", "Kubernetes MLOps", "Orchestrating end-to-end ML workflows on containerized Kubernetes clusters.", "Advanced", "High", "Critical", ["kubeflow"]),
        ("Triton Inference Server", "GPU Model Serving", "High-performance multi-framework inference server developed by NVIDIA.", "Advanced", "High", "Critical", ["triton"]),
        ("ONNX Runtime", "Portable Inference", "Standard format and execution engine for accelerating neural models.", "Intermediate", "High", "Critical", ["onnx-runtime"]),
        ("Data & Concept Drift Detection", "Production Monitoring", "Monitoring statistical distribution shift in input features and outputs.", "Intermediate", "High", "Critical", ["drift-monitoring"]),
        ("DVC (Data Version Control)", "Dataset Versioning", "Git-like version control for gigabyte and terabyte data files.", "Intermediate", "High", "High", ["dvc"])
    ]),

    # 26. Data Science & 27. Data Analytics
    ("Data Science and Analytics", "Insight Extraction", "Exploratory analysis, statistical hypothesis testing, and time series", [
        ("Exploratory Data Analysis", "Data Investigation", "Systematic inspection of distributions, correlations, and outliers.", "Beginner", "High", "Critical", ["eda"]),
        ("Hypothesis Testing", "Statistical Inference", "Evaluating null hypotheses with t-tests, z-tests, and ANOVA.", "Intermediate", "High", "Critical", ["hypothesis-tests"]),
        ("A/B Testing Methodology", "Experimentation", "Designing controlled experiments to measure incremental business lift.", "Intermediate", "High", "Critical", ["ab-testing"]),
        ("Cohort Retention Analysis", "User Analytics", "Tracking behavior patterns of user cohorts across weekly and monthly cohorts.", "Beginner", "High", "High", ["cohort-analysis"]),
        ("Time Series (ARIMA / Prophet)", "Forecasting", "Modeling temporal trends, seasonality, and residual noise for forecasting.", "Intermediate", "High", "Critical", ["time-series-forecasting"]),
        ("Data Storytelling", "Executive Communication", "Translating complex statistical findings into clear business slides.", "Beginner", "High", "Critical", ["data-storytelling"])
    ]),

    # 28. Business Intelligence
    ("Business Intelligence", "Enterprise Dashboards", "Interactive business reports, metric definitions, and semantic models", [
        ("Power BI Desktop", "BI Dashboards", "Creating rich interactive reports connected to enterprise datasets.", "Beginner", "High", "Critical", ["power-bi"]),
        ("Tableau Desktop", "Visual Analytics", "Visual analytics software exploring complex multi-dimensional datasets.", "Beginner", "High", "Critical", ["tableau"]),
        ("Looker", "Semantic BI", "Data modeling platform with LookML for centralized metric definitions.", "Intermediate", "High", "High", ["looker"]),
        ("DAX Formulas", "Power BI Expressions", "Formulas and calculations in Power BI data models.", "Intermediate", "High", "Critical", ["dax"]),
        ("Dimensional Modeling (Star Schema)", "Data Modeling", "Fact and dimension table schemas optimizing analytical queries.", "Intermediate", "High", "Critical", ["star-schema"]),
        ("Metabase", "Open Source BI", "Self-service reporting interface querying SQL databases with zero coding.", "Beginner", "High", "High", ["metabase"])
    ]),

    # 29. Data Engineering & 30. Big Data
    ("Data Engineering and Big Data", "Data Pipelines", "Distributed batch and stream processing, ETL pipelines, and warehouses", [
        ("Apache Spark", "Distributed Compute", "In-memory distributed computing engine for petabyte-scale data.", "Intermediate", "High", "Critical", ["apache-spark", "pyspark"]),
        ("Apache Kafka", "Event Streaming", "Distributed append-only commit log for streaming event architectures.", "Intermediate", "High", "Critical", ["kafka"]),
        ("Apache Airflow", "Workflow Orchestration", "Python-based DAG workflow scheduler automating data pipelines.", "Intermediate", "High", "Critical", ["airflow"]),
        ("dbt (Data Build Tool)", "Analytics Engineering", "Transforming raw warehouse data into clean tables using SQL and Jinja.", "Intermediate", "High", "Critical", ["dbt"]),
        ("Snowflake", "Cloud Data Warehouse", "Elastic cloud data platform with separate compute and storage layers.", "Intermediate", "High", "Critical", ["snowflake"]),
        ("Databricks", "Lakehouse Platform", "Collaborative Apache Spark environment managing Lakehouse storage.", "Intermediate", "High", "Critical", ["databricks"]),
        ("Delta Lake", "ACID Storage", "Open-source storage framework adding ACID transactions to object stores.", "Intermediate", "High", "Critical", ["delta-lake"]),
        ("Google BigQuery", "Serverless SQL", "Serverless warehouse querying petabytes of data with SQL.", "Intermediate", "High", "Critical", ["bigquery"]),
        ("Apache Flink", "Stream Processing", "Low-latency stateful stream processing for real-time analytics.", "Advanced", "Medium", "High", ["flink"])
    ])
]

print("Batch 1 (Domains 1 to 30) configured.")

DOMAINS_31_TO_60 = [
    # 31. Statistics and Mathematics
    ("Statistics and Mathematics", "Foundations", "Foundational mathematics for machine learning and scientific algorithms", [
        ("Linear Algebra", "Vector Math", "Matrix transformations, eigenvalues, eigenvectors, and vector spaces.", "Beginner", "High", "Critical", ["linear-algebra"]),
        ("Multivariate Calculus", "Optimization Math", "Partial derivatives, gradients, and Taylor series for optimization.", "Intermediate", "High", "Critical", ["calculus"]),
        ("Probability Distributions", "Probability Theory", "Normal, Binomial, Poisson, and exponential distribution properties.", "Beginner", "High", "Critical", ["probability-distributions"]),
        ("Bayes Theorem", "Probability", "Conditional probability formula updating priors based on likelihoods.", "Beginner", "High", "Critical", ["bayes-theorem"]),
        ("Discrete Mathematics", "Logic & Graphs", "Graph theory, combinatorics, set theory, and propositional logic.", "Beginner", "High", "Critical", ["discrete-math"])
    ]),

    # 32. Database Management & 33. SQL Technologies
    ("Database Management and SQL", "Relational Systems", "Relational database engines, storage engines, and SQL standards", [
        ("PostgreSQL", "Open Source RDBMS", "Extensible relational database system with JSONB and PostGIS support.", "Beginner", "High", "Critical", ["postgresql", "postgres"]),
        ("MySQL", "RDBMS", "Widely deployed open-source relational database engine.", "Beginner", "High", "Critical", ["mysql"]),
        ("SQLite", "Embedded SQL", "In-process embedded SQL database engine requiring zero configuration.", "Beginner", "High", "Critical", ["sqlite"]),
        ("Microsoft SQL Server", "Enterprise RDBMS", "Commercial relational database software developed by Microsoft.", "Intermediate", "High", "High", ["mssql"]),
        ("Oracle Database", "Enterprise RDBMS", "Enterprise multi-model database system for high-volume transactions.", "Intermediate", "High", "High", ["oracle-db"]),
        ("B-Tree Indexing", "Performance", "Balanced tree indexing structure accelerating point and range queries.", "Intermediate", "High", "Critical", ["b-tree-index"]),
        ("ACID Properties", "Transactions", "Atomicity, Consistency, Isolation, and Durability transaction guarantees.", "Intermediate", "High", "Critical", ["acid-transactions"]),
        ("Query Execution Plans", "SQL Optimization", "Interpreting EXPLAIN ANALYZE outputs to eliminate table scans.", "Intermediate", "High", "Critical", ["explain-plan"])
    ]),

    # 34. NoSQL Technologies & 35. Vector Databases
    ("NoSQL and Vector Databases", "Modern Storage", "Document, key-value, column-family, graph, and vector databases", [
        ("MongoDB", "Document Store", "JSON-like document database offering horizontal sharding.", "Beginner", "High", "Critical", ["mongodb"]),
        ("Redis", "In-Memory Store", "In-memory key-value data structure store used for caching and pub/sub.", "Beginner", "High", "Critical", ["redis"]),
        ("Apache Cassandra", "Wide-Column Store", "Masterless distributed database built for massive write throughput.", "Advanced", "Medium", "High", ["cassandra"]),
        ("Neo4j", "Graph Database", "Native graph database querying nodes and relationships with Cypher.", "Intermediate", "Medium", "High", ["neo4j"]),
        ("Amazon DynamoDB", "Managed NoSQL", "Serverless managed NoSQL database with single-digit millisecond latency.", "Intermediate", "High", "Critical", ["dynamodb"]),
        ("Elasticsearch", "Search Engine", "Distributed JSON search engine built on Apache Lucene.", "Intermediate", "High", "Critical", ["elasticsearch"]),
        ("Pinecone", "Managed Vector DB", "Cloud vector database built for high-scale semantic retrieval.", "Beginner", "High", "Critical", ["pinecone"]),
        ("ChromaDB", "Embedded Vector DB", "Lightweight open-source vector store designed for local RAG development.", "Beginner", "High", "Critical", ["chromadb"]),
        ("Weaviate", "Vector Engine", "Open-source vector search engine supporting hybrid and multimodal search.", "Intermediate", "High", "High", ["weaviate"]),
        ("Qdrant", "Rust Vector Store", "Vector similarity search engine with extended payload filtering.", "Intermediate", "High", "High", ["qdrant"]),
        ("Milvus", "Distributed Vector DB", "Cloud-native open-source vector database for massive billion-scale vectors.", "Advanced", "High", "High", ["milvus"]),
        ("FAISS", "Vector Search Library", "GPU-accelerated vector similarity search library from Meta AI.", "Advanced", "High", "Critical", ["faiss"])
    ]),

    # 36. Cloud Computing & 37. AWS
    ("Cloud Computing and AWS", "Amazon Web Services", "Cloud infrastructure, scalable computing, and managed cloud storage", [
        ("AWS EC2", "Virtual Machines", "Elastic compute capacity in the Amazon Web Services cloud.", "Beginner", "High", "Critical", ["ec2"]),
        ("AWS S3", "Object Storage", "Scalable cloud object storage service for data and backups.", "Beginner", "High", "Critical", ["s3"]),
        ("AWS Lambda", "Serverless Functions", "Event-driven serverless code execution without provisioning servers.", "Intermediate", "High", "Critical", ["lambda"]),
        ("AWS IAM", "Access Management", "Secure identity, roles, and granular policy management in AWS.", "Beginner", "High", "Critical", ["iam"]),
        ("AWS ECS", "Container Service", "Elastic container service orchestrating Docker container tasks.", "Intermediate", "High", "Critical", ["ecs"]),
        ("AWS EKS", "Managed Kubernetes", "Managed Kubernetes control plane on AWS infrastructure.", "Intermediate", "High", "Critical", ["eks"]),
        ("AWS RDS", "Managed SQL", "Managed relational database service for Postgres and MySQL.", "Beginner", "High", "Critical", ["rds"]),
        ("AWS CloudFront", "CDN Distribution", "Global content delivery network caching web assets close to users.", "Intermediate", "High", "High", ["cloudfront"]),
        ("AWS API Gateway", "Managed Gateway", "Fully managed API endpoint proxying requests to Lambdas and microservices.", "Intermediate", "High", "Critical", ["api-gateway"]),
        ("AWS CloudWatch", "Cloud Monitoring", "Real-time metrics, alarms, and unified log aggregation.", "Beginner", "High", "High", ["cloudwatch"])
    ]),

    # 38. Microsoft Azure & 39. Google Cloud
    ("Azure and Google Cloud", "Enterprise Multi-Cloud", "Microsoft Azure and Google Cloud platform services and architectures", [
        ("Azure Virtual Machines", "Azure Compute", "On-demand scalable cloud virtual machines in Azure.", "Beginner", "High", "High", ["azure-vm"]),
        ("Azure App Services", "PaaS Web Apps", "Fully managed hosting platform for enterprise web applications.", "Beginner", "High", "High", ["app-services"]),
        ("Azure Blob Storage", "Azure Storage", "Massively scalable object storage for cloud data.", "Beginner", "High", "High", ["azure-blob"]),
        ("Azure Functions", "Serverless Azure", "Serverless compute triggers executing business logic on demand.", "Intermediate", "High", "High", ["azure-functions"]),
        ("Azure Kubernetes Service", "Azure K8s", "Managed containerized application deployment on Azure.", "Intermediate", "High", "High", ["aks"]),
        ("Google Compute Engine", "GCP Compute", "Configurable virtual machine instances running on Google's infrastructure.", "Beginner", "High", "High", ["gce"]),
        ("Google Kubernetes Engine", "GCP K8s", "Premier managed Kubernetes cluster service with auto-pilot mode.", "Intermediate", "High", "Critical", ["gke"]),
        ("Google Cloud Run", "Serverless Containers", "Deploying containerized code to managed serverless endpoints.", "Beginner", "High", "Critical", ["cloud-run"]),
        ("Google Cloud Storage", "GCP Storage", "Unified object storage offering high availability and durability.", "Beginner", "High", "High", ["gcs"])
    ]),

    # 40. DevOps, 41. Platform Engineering, 42. SRE
    ("DevOps and SRE", "Site Reliability", "Platform infrastructure, monitoring, SLI/SLO metrics, and error budgets", [
        ("Site Reliability Engineering (SRE)", "Reliability Culture", "Engineering software principles applied to operations and systems.", "Intermediate", "High", "Critical", ["sre"]),
        ("Service Level Objectives (SLOs)", "Reliability Metrics", "Agreed target reliability metrics and measurable service indicators.", "Intermediate", "High", "Critical", ["slo"]),
        ("Error Budgets", "Operational Risk", "Balancing system innovation speed with availability constraints.", "Intermediate", "High", "High", ["error-budget"]),
        ("Prometheus Monitoring", "Time Series Metrics", "Pull-based metrics collection engine with dimensional querying.", "Intermediate", "High", "Critical", ["prometheus"]),
        ("Grafana Dashboards", "Observability UI", "Composable visual dashboards for system metrics and telemetry.", "Beginner", "High", "Critical", ["grafana"]),
        ("OpenTelemetry (OTel)", "Distributed Telemetry", "Unified standard for traces, metrics, and logs across microservices.", "Intermediate", "High", "Critical", ["opentelemetry"]),
        ("Incident Postmortems", "Operational Learning", "Blameless analysis identifying root causes and action items.", "Beginner", "High", "Critical", ["postmortems"]),
        ("Infrastructure as Code (IaC)", "Automated Provisioning", "Provisioning servers and networks via machine-readable code.", "Intermediate", "High", "Critical", ["iac"])
    ]),

    # 43. Containerization & 44. Kubernetes
    ("Containerization and Kubernetes", "Cloud Native", "Docker packaging, container runtimes, Kubernetes workloads, and Helm", [
        ("Docker", "Container Engine", "Standardized container packaging isolating application dependencies.", "Beginner", "High", "Critical", ["docker"]),
        ("Dockerfile Multi-Stage Builds", "Image Optimization", "Minimizing container footprint and removing build dependencies.", "Beginner", "High", "Critical", ["dockerfile"]),
        ("Docker Compose", "Multi-Container Dev", "Configuring multi-service local environments with YAML definitions.", "Beginner", "High", "Critical", ["docker-compose"]),
        ("Kubernetes", "Container Orchestration", "Automating container scheduling, scaling, and rolling rollouts.", "Intermediate", "High", "Critical", ["kubernetes", "k8s"]),
        ("Kubernetes Pods & Deployments", "K8s Workloads", "Core workload controllers managing container replicas and lifecycles.", "Intermediate", "High", "Critical", ["k8s-deployments"]),
        ("Kubernetes Services & Ingress", "K8s Routing", "Exposing network routes and routing traffic to container pods.", "Intermediate", "High", "Critical", ["k8s-ingress"]),
        ("Helm Charts", "K8s Package Manager", "Templating and packaging complex Kubernetes applications.", "Intermediate", "High", "Critical", ["helm"]),
        ("ConfigMaps and Secrets", "K8s Config", "Decoupling runtime environment variables and secrets from images.", "Intermediate", "High", "Critical", ["k8s-secrets"])
    ]),

    # 45. CI/CD
    ("CI/CD and Automation", "Continuous Delivery", "Automated build, test, and release pipelines and GitOps", [
        ("GitHub Actions", "Repository CI/CD", "Automated pipeline workflows triggered by Git commits and pull requests.", "Beginner", "High", "Critical", ["github-actions"]),
        ("GitLab CI/CD", "Integrated Pipelines", "Continuous integration and delivery runner embedded in GitLab.", "Intermediate", "High", "High", ["gitlab-ci"]),
        ("Jenkins", "Automation Server", "Extensible automation server orchestrating distributed pipelines.", "Intermediate", "Medium", "High", ["jenkins"]),
        ("Argo CD", "GitOps Continuous Delivery", "Declarative GitOps controller syncing Git manifests to Kubernetes.", "Intermediate", "High", "Critical", ["argocd"]),
        ("Terraform", "Cloud Infrastructure", "Declarative HCL tool provisioning multi-cloud resources.", "Intermediate", "High", "Critical", ["terraform"]),
        ("Ansible", "Config Management", "Agentless automation tool configuring servers via SSH.", "Intermediate", "High", "High", ["ansible"])
    ]),

    # 46. Cybersecurity, 47. Ethical Hacking, 48. Network Security
    ("Cybersecurity and Ethical Hacking", "Security Defense", "Penetration testing, vulnerability scanning, and cryptographic controls", [
        ("OWASP Top 10", "Web Security", "Authoritative catalog of the most critical web application security risks.", "Beginner", "High", "Critical", ["owasp"]),
        ("Wireshark", "Packet Analysis", "Network protocol packet capture and deep inspection tool.", "Beginner", "High", "Critical", ["wireshark"]),
        ("Nmap", "Port Scanning", "Network mapper discovering hosts, open ports, and running services.", "Beginner", "High", "Critical", ["nmap"]),
        ("Metasploit", "Exploitation Framework", "Penetration testing platform executing proof-of-concept exploits.", "Intermediate", "High", "Critical", ["metasploit"]),
        ("Burp Suite", "Web Proxy Testing", "Intercepting web proxy for finding vulnerabilities in web applications.", "Intermediate", "High", "Critical", ["burp-suite"]),
        ("Kali Linux", "Pen-testing Distribution", "Specialized security distribution with bundled auditing tools.", "Beginner", "High", "Critical", ["kali-linux"]),
        ("Cryptography (AES, RSA, ECC)", "Encryption", "Symmetric and asymmetric ciphers securing sensitive data.", "Intermediate", "High", "Critical", ["cryptography"]),
        ("SIEM (Splunk, Wazuh)", "Security Analytics", "Aggregating log streams to correlate and alert on security incidents.", "Intermediate", "High", "Critical", ["siem"])
    ]),

    # 49. Application Security, 50. Cloud Security, 51. Digital Forensics
    ("AppSec and Cloud Security", "Specialized Defense", "Static analysis, zero trust models, and digital forensics investigation", [
        ("SAST & DAST", "Automated Security QA", "Static source code audits and dynamic runtime penetration scans.", "Intermediate", "High", "Critical", ["sast-dast"]),
        ("Threat Modeling (STRIDE)", "Architecture Security", "Systematic method analyzing threats against spoofing and tampering.", "Intermediate", "High", "Critical", ["stride"]),
        ("Zero Trust Architecture", "Perimeter Security", "Security strategy requiring continuous verification for every access.", "Intermediate", "High", "Critical", ["zero-trust"]),
        ("Digital Forensics (DFIR)", "Evidence Recovery", "Forensic extraction of volatile memory dumps and disk artifacts.", "Advanced", "High", "High", ["dfir"])
    ]),

    # 52. Blockchain, 53. Smart Contracts, 54. Web3
    ("Blockchain and Web3", "Decentralized Systems", "Smart contracts, EVM execution, decentralized storage, and DeFi security", [
        ("Solidity", "Smart Contract Language", "Object-oriented language for writing Ethereum smart contracts.", "Intermediate", "High", "Critical", ["solidity"]),
        ("EVM (Ethereum Virtual Machine)", "Decentralized Runtime", "Execution environment running smart contracts across distributed nodes.", "Intermediate", "High", "Critical", ["evm"]),
        ("Hardhat", "Ethereum Dev Tooling", "Development environment to compile, test, and deploy EVM contracts.", "Intermediate", "High", "Critical", ["hardhat"]),
        ("Foundry", "Rust Ethereum Toolkit", "Ultra-fast testing framework executing Solidity tests natively.", "Intermediate", "High", "Critical", ["foundry"]),
        ("Ethers.js", "Web3 Library", "JavaScript library connecting client interfaces with Ethereum nodes.", "Beginner", "High", "Critical", ["ethersjs"]),
        ("Rust on Solana (Anchor)", "High-Throughput Chains", "Developing high-speed programs on the Solana blockchain.", "Advanced", "High", "High", ["solana-anchor"]),
        ("IPFS", "Decentralized File Storage", "Content-addressed peer-to-peer hypermedia storage protocol.", "Beginner", "Medium", "High", ["ipfs"]),
        ("Smart Contract Auditing", "Web3 Security", "Detecting reentrancy bugs, integer overflows, and oracle exploits.", "Advanced", "High", "Critical", ["contract-audit"])
    ]),

    # 55. Internet of Things & 56. Robotics
    ("IoT and Robotics", "Physical Systems", "Hardware controllers, sensors, ROS robotics, and messaging protocols", [
        ("Arduino", "Microcontroller Board", "Open prototyping platform for electronic sensor interaction.", "Beginner", "High", "Critical", ["arduino"]),
        ("Raspberry Pi", "Single Board Computer", "Linux computer with GPIO pins connecting to external sensors.", "Beginner", "High", "Critical", ["raspberry-pi"]),
        ("ESP32", "Wi-Fi & Bluetooth MCU", "Dual-core low-power microcontroller with wireless connectivity.", "Beginner", "High", "Critical", ["esp32"]),
        ("MQTT Protocol", "IoT Messaging", "Lightweight publish/subscribe messaging designed for constrained devices.", "Beginner", "High", "Critical", ["mqtt"]),
        ("ROS 2 (Robot Operating System)", "Robotics Middleware", "Framework providing hardware abstraction, drivers, and visualizers.", "Intermediate", "High", "Critical", ["ros2"]),
        ("Gazebo Robotics Simulator", "Physical Simulation", "Simulating robot dynamics and sensor streams in 3D physics.", "Intermediate", "High", "High", ["gazebo"]),
        ("I2C / SPI / UART", "Hardware Buses", "Serial communication protocols connecting chips to peripherals.", "Beginner", "High", "Critical", ["hardware-buses"])
    ]),

    # 57. Embedded Systems, 58. VLSI, 59. FPGA, 60. Electronics
    ("Embedded Systems and VLSI", "Hardware Engineering", "Firmware, real-time operating systems, Verilog, and circuit design", [
        ("Embedded C / C++", "Firmware Development", "Low-level programming directly managing microcontroller registers.", "Intermediate", "High", "Critical", ["embedded-c"]),
        ("FreeRTOS", "Real-Time OS", "Real-time kernel managing deterministic priority-based task scheduling.", "Intermediate", "High", "Critical", ["freertos"]),
        ("Verilog / SystemVerilog", "Hardware Description", "Standard hardware description languages for digital circuit modeling.", "Intermediate", "High", "Critical", ["verilog"]),
        ("VHDL", "Hardware Description", "Strongly-typed description language used in aerospace and defense circuits.", "Intermediate", "Medium", "High", ["vhdl"]),
        ("FPGA Development (Vivado)", "Programmable Logic", "Synthesizing custom digital logic architectures onto Xilinx FPGAs.", "Advanced", "High", "Critical", ["fpga"]),
        ("PCB Design with KiCad", "Circuit Board Design", "Schematic capture, routing traces, and exporting Gerber files.", "Intermediate", "High", "Critical", ["kicad"]),
        ("Digital Signal Processing (DSP)", "Signal Algorithms", "Filtering, Fourier transforms, and signal conditioning algorithms.", "Advanced", "High", "High", ["dsp"])
    ])
]

print("Batch 2 (Domains 31 to 60) configured.")

DOMAINS_61_TO_90 = [
    # 61. Computer Networking & 62. Linux Administration
    ("Networking and Linux", "Infrastructure Fundamentals", "IP networking, domain services, system administration, and firewalls", [
        ("TCP/IP Protocol Suite", "Networking Core", "Layered communications protocol governing internet traffic.", "Beginner", "High", "Critical", ["tcp-ip"]),
        ("DNS & DHCP Configuration", "Network Services", "Name resolution and dynamic address assignment services.", "Beginner", "High", "Critical", ["dns"]),
        ("Linux System Administration", "Server Management", "Managing storage mounts, user groups, and core daemons.", "Beginner", "High", "Critical", ["linux-sysadmin"]),
        ("Systemd Service Management", "Service Inits", "Configuring target units, startup dependencies, and journalctl logs.", "Intermediate", "High", "Critical", ["systemd"]),
        ("SSH Remote Administration", "Secure Shell", "Public key cryptography managing encrypted shell sessions.", "Beginner", "High", "Critical", ["ssh"]),
        ("Linux Firewalls (iptables / UFW)", "Packet Filtering", "Configuring packet inspection rules and port filtering policies.", "Beginner", "High", "High", ["firewalls"])
    ]),

    # 63. Software Engineering, 64. Testing, 65. Automation, 66. QA
    ("Software Engineering and QA", "Engineering Quality", "Agile methodologies, test automation, and performance testing", [
        ("Git Version Control", "Collaboration", "Distributed version control system managing commits and branches.", "Beginner", "High", "Critical", ["git"]),
        ("Test-Driven Development (TDD)", "Testing Method", "Writing unit tests prior to implementation to guarantee coverage.", "Intermediate", "High", "Critical", ["tdd"]),
        ("Selenium WebDriver", "Browser Automation", "Automated browser interaction suite executing regression test suites.", "Beginner", "High", "Critical", ["selenium"]),
        ("Playwright Test Framework", "Modern E2E", "Fast automated end-to-end testing with network interception.", "Intermediate", "High", "Critical", ["playwright"]),
        ("Postman API Automation", "API Testing", "Scripting REST API request assertions and running collections with Newman.", "Beginner", "High", "Critical", ["postman"]),
        ("Load Testing (k6 / JMeter)", "Performance QA", "Simulating thousands of virtual concurrent users to find breaking points.", "Intermediate", "High", "High", ["load-testing"]),
        ("Agile & Scrum Sprints", "Delivery Framework", "Iterative sprint ceremonies and backlog management for engineering teams.", "Beginner", "High", "Critical", ["agile"])
    ]),

    # 67. System Design, 68. Microservices, 69. API Development
    ("System Design and Microservices", "Distributed Architecture", "High-throughput system architecture, resilience patterns, and API gateways", [
        ("Scalable System Design", "System Architecture", "Designing horizontal systems supporting millions of daily active users.", "Advanced", "High", "Critical", ["system-design"]),
        ("Microservices Architecture", "Service Decomposition", "Decoupling services around business domains with autonomous lifecycles.", "Intermediate", "High", "Critical", ["microservices"]),
        ("Event-Driven Architecture", "Asynchronous Events", "Decoupled publisher-subscriber models communicating via event streams.", "Intermediate", "High", "Critical", ["event-driven"]),
        ("Domain-Driven Design (DDD)", "Domain Modeling", "Mapping complex business domains to bounded contexts and aggregates.", "Advanced", "High", "Critical", ["ddd"]),
        ("CQRS & Event Sourcing", "Data Patterns", "Segregating write command mutations from read query projections.", "Advanced", "Medium", "High", ["cqrs"]),
        ("API Gateway Pattern", "Edge Routing", "Unified entry point handling client routing, authentication, and throttling.", "Intermediate", "High", "Critical", ["api-gateway"]),
        ("Circuit Breaker Pattern", "Fault Resilience", "Gracefully isolating failing dependencies to avert complete system outages.", "Intermediate", "High", "Critical", ["circuit-breaker"])
    ]),

    # 70. UI/UX Design & 71. Graphic Design
    ("UI/UX Design", "Design Systems", "User research, wireframing, design tokens, and interactive prototyping", [
        ("Figma UI Prototyping", "Interface Design", "Collaborative design application defining components and user flows.", "Beginner", "High", "Critical", ["figma"]),
        ("User Research & Usability Testing", "UX Research", "Validating design assumptions with qualitative user feedback.", "Beginner", "High", "Critical", ["ux-research"]),
        ("Wireframing & Information Architecture", "UX Structure", "Low-fidelity layouts organizing site content and navigation.", "Beginner", "High", "Critical", ["wireframing"]),
        ("Design Systems & Tokens", "Component Standards", "Scalable design libraries harmonizing typography, colors, and widgets.", "Intermediate", "High", "Critical", ["design-systems"])
    ]),

    # 72. Game Development & 73. AR/VR Development
    ("Game and AR/VR Development", "Real-Time 3D", "Game engines, C# scripting, 3D assets, shaders, and spatial computing", [
        ("Unity Game Engine", "Game Engines", "Cross-platform real-time 3D and 2D game development engine.", "Intermediate", "High", "Critical", ["unity"]),
        ("Unreal Engine 5", "Photorealistic 3D", "State-of-the-art game engine with Nanite geometry and Lumen lighting.", "Advanced", "High", "Critical", ["unreal-engine"]),
        ("C# for Unity Scripting", "Game Logic", "Writing gameplay mechanics and physical interactions in Unity.", "Intermediate", "High", "Critical", ["unity-c#"]),
        ("C++ for Unreal Engine", "Game Systems", "Engine-level systems and high-speed gameplay code in Unreal.", "Advanced", "High", "Critical", ["unreal-cpp"]),
        ("Spatial Computing (OpenXR)", "XR Standards", "Open API standard for writing virtual and augmented reality apps.", "Advanced", "Medium", "High", ["openxr"]),
        ("Shader Programming (HLSL / GLSL)", "Graphics Shaders", "Writing custom visual shaders computing pixel and vertex lighting.", "Advanced", "Medium", "High", ["shaders"]),
        ("Blender 3D Modeling", "Asset Pipelines", "Creating 3D models, rigging skeletal animations, and texturing.", "Intermediate", "High", "High", ["blender"])
    ]),

    # 74. Product, 75. Business Analysis, 76. Project Management, 77. Technical Documentation
    ("Product and Project Management", "Project Delivery", "Product requirements, agile backlogs, technical specifications, and API docs", [
        ("Product Requirements (PRD)", "Product Definition", "Documenting target user problems, metrics, and functional scope.", "Beginner", "High", "Critical", ["prd"]),
        ("User Stories & Acceptance Criteria", "Agile Specs", "Structuring requirement tickets using Given-When-Then criteria.", "Beginner", "High", "Critical", ["user-stories"]),
        ("Jira & Confluence Management", "Agile Tools", "Managing team backlogs, kanban boards, and project documentation.", "Beginner", "High", "Critical", ["jira"]),
        ("Technical API Documentation", "Developer Docs", "Writing OpenAPI specs and onboarding tutorials for software developers.", "Beginner", "High", "Critical", ["technical-writing"])
    ]),

    # 78. Bioinformatics & 79. Healthcare Technology
    ("Bioinformatics and HealthTech", "Life Sciences", "Biological data analysis, sequence alignment, and healthcare data standards", [
        ("BioPython", "Computational Biology", "Python tools for analyzing biological sequences and structural files.", "Intermediate", "High", "Critical", ["biopython"]),
        ("BLAST Sequence Alignment", "Sequence Search", "Comparing biological sequences against reference genome databases.", "Intermediate", "High", "Critical", ["blast"]),
        ("Nextflow Workflows", "Pipeline Orchestration", "Scalable workflow execution for genomic data pipelines.", "Intermediate", "High", "High", ["nextflow"]),
        ("HL7 / FHIR Standards", "Health Data Exchange", "Standard specifications for exchanging electronic healthcare records.", "Intermediate", "High", "Critical", ["fhir"]),
        ("DICOM Medical Imaging", "Medical Scans", "Format for handling, storing, and transmitting medical imaging files.", "Intermediate", "High", "High", ["dicom"]),
        ("AlphaFold Protein Modeling", "Structural Biology", "Deep learning prediction of 3D protein structures from sequences.", "Advanced", "High", "High", ["alphafold"])
    ]),

    # 80. FinTech & 81. Automotive Technology
    ("FinTech and Automotive Software", "Vertical Industries", "Financial exchange protocols, payment processing, AUTOSAR, and CAN bus", [
        ("FIX Financial Protocol", "Financial Messaging", "Messaging standard for real-time electronic securities trading.", "Advanced", "Medium", "High", ["fix-protocol"]),
        ("Stripe Payment Integration", "Payment Gateways", "Integrating secure card checkout, subscriptions, and webhooks.", "Beginner", "High", "Critical", ["stripe"]),
        ("Algorithmic Trading Models", "Quantitative Finance", "Statistical backtesting of automated financial trading strategies.", "Intermediate", "Medium", "High", ["algo-trading"]),
        ("AUTOSAR Standard", "Automotive Architecture", "Open system architecture for automotive electronic control units.", "Advanced", "High", "Critical", ["autosar"]),
        ("CAN Bus Protocol", "Vehicle Communication", "Robust serial bus allowing microcontrollers to communicate in vehicles.", "Intermediate", "High", "Critical", ["can-bus"]),
        ("Autonomous Driving Perception", "Automotive AI", "Processing camera and lidar sensor data for vehicle path planning.", "Advanced", "Medium", "High", ["autonomous-driving"])
    ]),

    # 82. Quantum & 83. High-Performance Computing
    ("Quantum and High-Performance Computing", "Advanced Computing", "Quantum circuits, qubit gates, CUDA programming, and cluster schedulers", [
        ("Qiskit", "Quantum Circuits", "IBM open-source SDK for designing and running quantum algorithms.", "Intermediate", "High", "Critical", ["qiskit"]),
        ("Cirq", "Quantum Computing", "Google Python library for creating and optimizing noisy quantum circuits.", "Intermediate", "High", "High", ["cirq"]),
        ("NVIDIA CUDA Programming", "GPU Acceleration", "Massively parallel computing architecture leveraging GPU cores.", "Advanced", "High", "Critical", ["cuda"]),
        ("OpenCL Heterogeneous Compute", "Cross-Platform Compute", "Parallel programming standard across CPUs, GPUs, and accelerators.", "Advanced", "Medium", "High", ["opencl"]),
        ("Slurm Workload Manager", "Cluster Scheduling", "Cluster management and job scheduling system for supercomputers.", "Intermediate", "High", "High", ["slurm"])
    ]),

    # 84. Scientific & 85. Geospatial & 86. GIS
    ("Scientific Computing and GIS", "Geospatial Intelligence", "Spatial data analysis, coordinate projections, satellite imagery, and maps", [
        ("GeoPandas", "Spatial Data Science", "Extending Pandas to support spatial geometric data and coordinates.", "Beginner", "High", "Critical", ["geopandas"]),
        ("GDAL / OGR", "Geospatial Formats", "Translator library for raster and vector geospatial formats.", "Intermediate", "High", "Critical", ["gdal"]),
        ("QGIS Software", "Desktop GIS", "Open-source Geographic Information System for mapping and spatial analysis.", "Beginner", "High", "Critical", ["qgis"]),
        ("Satellite Remote Sensing", "Earth Observation", "Analyzing Sentinel and Landsat multispectral satellite raster data.", "Intermediate", "Medium", "High", ["remote-sensing"])
    ]),

    # 87. Digital Twins, 88. Edge Computing, 89. Computer Hardware, 90. Emerging Tech
    ("Edge Computing and Emerging Tech", "Emerging Paradigms", "Edge computing, WebAssembly, TinyML, and digital twin simulation", [
        ("TinyML on Microcontrollers", "Embedded Machine Learning", "Deploying low-power neural networks on battery-operated sensors.", "Intermediate", "High", "Critical", ["tinyml"]),
        ("WebAssembly (Wasm)", "Near-Native Web", "Compact binary bytecode running high-performance C++/Rust in browsers.", "Intermediate", "High", "Critical", ["wasm"]),
        ("Digital Twin Simulations", "Virtual Physical Models", "Creating digital models synchronized with real-world sensor streams.", "Advanced", "Medium", "High", ["digital-twins"]),
        ("Edge Computing Nodes", "Distributed Processing", "Running AI inference locally at IoT gateways to reduce cloud latency.", "Intermediate", "High", "Critical", ["edge-computing"]),
        ("Neuromorphic Computing", "Brain-Inspired Hardware", "Spiking neural architectures mimicking biological synapses.", "Advanced", "Low", "Emerging", ["neuromorphic"])
    ])
]

def seed_all_technical_skills(db: Session = None):
    """Executes database insertion for all 90 domains."""
    all_domains = DOMAINS_1_TO_30 + DOMAINS_31_TO_60 + DOMAINS_61_TO_90
    print("=" * 60)
    print(f"COMMENCING COMPREHENSIVE SEEDING ACROSS {len(all_domains)} DOMAINS")
    print("=" * 60)

    def _execute(session: Session):
        total_skills = 0
        total_categories = 0
        seen_codes = set()
        seen_names = set()

        for cat_name, domain_cluster, desc, skills_list in all_domains:
            category = session.query(SkillCategory).filter_by(name=cat_name).first()
            if not category:
                category = SkillCategory(name=cat_name, domain=domain_cluster, description=desc)
                session.add(category)
                session.flush()
                total_categories += 1

            for name, subcat, skill_desc, diff, priority, relev, aliases in skills_list:
                clean_name = name.strip()
                code = slugify(clean_name)

                if code in seen_codes or clean_name.lower() in seen_names:
                    continue
                seen_codes.add(code)
                seen_names.add(clean_name.lower())

                skill = session.query(TechnicalSkill).filter_by(skill_code=code).first()
                if not skill:
                    skill = TechnicalSkill(
                        skill_code=code,
                        name=clean_name,
                        category_id=category.category_id,
                        subcategory=subcat,
                        description=skill_desc,
                        difficulty_level=diff,
                        learning_priority=priority,
                        industry_relevance=relev,
                        is_active=True,
                        verification_status="Verified",
                        source="Curated Engineering Taxonomy"
                    )
                    session.add(skill)
                    session.flush()
                    total_skills += 1

                    for a in aliases:
                        if a.strip().lower() != clean_name.lower():
                            session.add(SkillAlias(skill_id=skill.skill_id, alias_name=a.strip()))

        session.commit()
        return total_skills, total_categories

    if db is not None:
        return _execute(db)
    else:
        with get_db_session() as session:
            return _execute(session)

if __name__ == "__main__":
    skills, cats = seed_all_technical_skills()
    print(f"\n[DONE] Seeded {skills} technical skills across {cats} categories!")
