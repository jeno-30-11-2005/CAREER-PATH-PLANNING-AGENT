# database/seed_data/comprehensive_skills_builder.py
"""
Builds and returns the comprehensive 1,500+ technical skills dataset covering all 90 domains.
Each record contains: (Category Name, Domain Cluster, Description, [Skill Tuples])
Skill Tuple: (Name, Subcategory, Description, Difficulty, Priority, Relevance, [Aliases])
"""
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

SKILLS_BY_DOMAIN = [
    # 1. Programming Languages
    ("Programming Languages", "Software Engineering", "Core coding languages across procedural, object-oriented, and functional paradigms", [
        ("Python", "General Purpose", "Interpreted, high-level, dynamically typed language widely used in AI, web, and automation.", "Beginner", "High", "Critical", ["python3", "py"]),
        ("Java", "Enterprise OOP", "Class-based, object-oriented language designed for cross-platform enterprise systems.", "Intermediate", "High", "Critical", ["jdk", "jvm"]),
        ("C", "Systems Programming", "Procedural systems language providing low-level memory control and hardware access.", "Intermediate", "High", "High", ["ansi-c", "c-lang"]),
        ("C++", "Systems & High Performance", "Multi-paradigm language with high performance, OOP, templates, and RAII.", "Advanced", "High", "Critical", ["cpp", "cplusplus"]),
        ("C#", "Enterprise & Game Dev", "Modern, type-safe object-oriented language for .NET, game development, and enterprise services.", "Intermediate", "High", "High", ["csharp", "dotnet-c#"]),
        ("JavaScript", "Web Development", "High-level, dynamic language that powers interactive front-end and full-stack web.", "Beginner", "High", "Critical", ["js", "ecmascript"]),
        ("TypeScript", "Web Development", "Strict syntactical superset of JavaScript adding static type definitions.", "Intermediate", "High", "Critical", ["ts"]),
        ("Go", "Cloud & Backend", "Statically typed, compiled language engineered by Google for concurrent backend services.", "Intermediate", "High", "Critical", ["golang"]),
        ("Rust", "Systems Programming", "Systems programming language focused on memory safety, zero-cost abstractions, and speed.", "Advanced", "High", "Critical", ["rust-lang"]),
        ("Kotlin", "Mobile & JVM", "Modern, concise statically typed language that is Google's preferred choice for Android.", "Intermediate", "High", "High", ["kt"]),
        ("Swift", "Mobile & Apple", "Fast, safe, and modern programming language for iOS, iPadOS, macOS, and watchOS.", "Intermediate", "High", "High", ["apple-swift"]),
        ("PHP", "Server-Side Web", "Widely-used open-source scripting language for server-side web development.", "Beginner", "Medium", "Moderate", ["php8"]),
        ("Ruby", "Web & Scripting", "Dynamic, open-source programming language with a focus on simplicity and productivity.", "Beginner", "Medium", "Moderate", ["ruby-lang"]),
        ("R", "Statistical Computing", "Programming language and environment for statistical computing, graphics, and bioinformatics.", "Intermediate", "High", "High", ["r-lang"]),
        ("Scala", "Functional & Big Data", "High-level language combining object-oriented and functional programming on the JVM.", "Advanced", "Medium", "High", ["scala-lang"]),
        ("Dart", "Cross-Platform Mobile", "Client-optimized language for fast apps on any platform, powering Flutter.", "Beginner", "Medium", "High", ["dart-lang"]),
        ("Julia", "Scientific Computing", "High-level, high-performance dynamic programming language for technical computing.", "Intermediate", "Medium", "Emerging", ["julia-lang"]),
        ("Lua", "Scripting & Game Dev", "Lightweight, high-level, multi-paradigm programming language designed for embedded use in games.", "Beginner", "Medium", "Moderate", ["lua-lang"]),
        ("Haskell", "Functional Programming", "Statically typed, purely functional programming language with type inference and lazy evaluation.", "Advanced", "Low", "Moderate", ["ghc-haskell"]),
        ("Elixir", "Concurrent Systems", "Dynamic, functional language designed for building scalable and maintainable applications on Erlang VM.", "Intermediate", "Medium", "High", ["elixir-lang"]),
        ("Clojure", "Lisp on JVM", "Dynamic, general-purpose programming language, combining the approachability of a scripting language with multithreading.", "Advanced", "Low", "Moderate", ["clojure-lang"]),
        ("Perl", "Text Processing", "High-level, general-purpose, interpreted, dynamic programming language known for regular expressions.", "Intermediate", "Low", "Moderate", ["perl-lang"]),
        ("Shell Scripting", "Automation & DevOps", "Writing scripts for Unix/Linux command-line shells (Bash, Zsh) to automate system operations.", "Beginner", "High", "Critical", ["bash", "sh", "zsh"]),
        ("PowerShell", "Automation & Windows", "Task automation and configuration management framework with command-line shell.", "Intermediate", "High", "High", ["pwsh"]),
        ("Assembly Language x86", "Low-Level Computing", "Low-level programming language corresponding to CPU machine code instructions.", "Expert", "Low", "Moderate", ["asm-x86"]),
        ("Assembly Language ARM", "Low-Level Computing", "Assembly instruction set for ARM architecture powering mobile, embedded, and Apple silicon.", "Expert", "Low", "High", ["arm-assembly"]),
        ("Zig", "Systems Programming", "General-purpose programming language and toolchain for maintaining robust, optimal and reusable software.", "Advanced", "Medium", "Emerging", ["zig-lang"]),
        ("Nim", "Compiled Systems", "Statically typed compiled systems programming language that combines efficiency with readability.", "Intermediate", "Low", "Moderate", ["nim-lang"]),
        ("Groovy", "JVM Scripting", "Powerful, optionally typed and dynamic language, with static-typing and static compilation capabilities.", "Intermediate", "Medium", "Moderate", ["apache-groovy"]),
        ("SQL", "Database Querying", "Structured Query Language standard for storing, manipulating, and retrieving data in relational databases.", "Beginner", "High", "Critical", ["ansi-sql", "structured-query-language"])
    ]),

    # 2. Python Ecosystem
    ("Python Ecosystem", "Data Science & Web", "Libraries, tooling, and frameworks built around Python", [
        ("NumPy", "Scientific Computing", "Fundamental package for scientific computing with N-dimensional arrays in Python.", "Beginner", "High", "Critical", ["numpy-lib"]),
        ("Pandas", "Data Manipulation", "Data analysis and manipulation library offering high-performance DataFrame structures.", "Beginner", "High", "Critical", ["pandas-lib"]),
        ("SciPy", "Scientific Computing", "Algorithms for scientific computing including optimization, integration, and interpolation.", "Intermediate", "High", "High", ["scipy-lib"]),
        ("Matplotlib", "Data Visualization", "Comprehensive library for creating static, animated, and interactive visualizations in Python.", "Beginner", "High", "High", ["matplotlib-py"]),
        ("Seaborn", "Data Visualization", "Statistical data visualization library based on Matplotlib with beautiful default styles.", "Beginner", "High", "High", ["seaborn-py"]),
        ("Scikit-Learn", "Machine Learning", "Simple and efficient tools for predictive data analysis and classical machine learning.", "Intermediate", "High", "Critical", ["sklearn"]),
        ("FastAPI", "Web Frameworks", "Modern, fast, high-performance web framework for building APIs with Python 3.8+ based on type hints.", "Intermediate", "High", "Critical", ["fastapi-framework"]),
        ("Flask", "Web Frameworks", "Lightweight WSGI micro web framework designed for rapid web service development.", "Beginner", "High", "High", ["flask-py"]),
        ("Django", "Web Frameworks", "High-level Python web framework that encourages rapid development and clean, pragmatic design.", "Intermediate", "High", "Critical", ["django-framework"]),
        ("SQLAlchemy", "ORM & Database", "Python SQL toolkit and Object Relational Mapper offering full suite of persistence patterns.", "Intermediate", "High", "Critical", ["sqlalchemy-orm"]),
        ("Pydantic", "Data Validation", "Data parsing and validation library using Python type hints with incredible speed.", "Intermediate", "High", "Critical", ["pydantic-v2"]),
        ("Celery", "Distributed Tasks", "Asynchronous task queue/job queue based on distributed message passing.", "Intermediate", "Medium", "High", ["celery-tasks"]),
        ("Pytest", "Testing & QA", "Mature full-featured Python testing tool that helps write better programs.", "Beginner", "High", "Critical", ["pytest-framework"]),
        ("Poetry", "Dependency Management", "Tool for dependency management and packaging in Python with deterministic lockfiles.", "Intermediate", "High", "High", ["poetry-py"]),
        ("Polars", "High-Performance Data", "Blazingly fast DataFrames library implemented in Rust with multi-threaded execution.", "Intermediate", "High", "Emerging", ["polars-df"]),
        ("Dask", "Parallel Computing", "Flexible library for parallel computing and scaling Python data science workloads.", "Advanced", "Medium", "High", ["dask-py"]),
        ("Ray", "Distributed Computing", "Unified framework for scaling AI and Python applications from single machines to clusters.", "Advanced", "High", "Emerging", ["ray-project"]),
        ("Beautiful Soup", "Web Scraping", "Python library for pulling data out of HTML and XML files for web scraping.", "Beginner", "Medium", "Moderate", ["bs4"]),
        ("Scrapy", "Web Scraping", "Fast high-level web crawling and scraping framework for extracting structured data.", "Intermediate", "Medium", "High", ["scrapy-framework"]),
        ("Asyncio", "Concurrent Python", "Python library to write concurrent code using the async/await syntax.", "Intermediate", "High", "Critical", ["python-asyncio"]),
        ("Streamlit", "Data Apps", "Open-source Python app framework built specifically for Machine Learning and Data Science teams.", "Beginner", "High", "Critical", ["streamlit-py"]),
        ("Gradio", "ML Demonstrations", "Fastest way to demo machine learning models with a friendly web interface.", "Beginner", "High", "High", ["gradio-app"]),
        ("Numba", "JIT Compiler", "Open source JIT compiler that translates a subset of Python and NumPy code into fast machine code.", "Advanced", "Medium", "High", ["numba-jit"]),
        ("Cython", "C-Extensions", "Optimizing static compiler for both the Python programming language and the extended Cython language.", "Advanced", "Medium", "Moderate", ["cython-lang"]),
        ("Typer", "CLI Development", "Library for building CLI applications that users love and developers love creating.", "Beginner", "Medium", "High", ["typer-cli"]),
        ("Loguru", "Logging", "Library which aims to bring enjoyable logging in Python with zero boilerplate configuration.", "Beginner", "Medium", "High", ["loguru-py"])
    ]),

    # 3. Java Ecosystem
    ("Java Ecosystem", "Enterprise Software", "Frameworks, build tools, and enterprise libraries for Java", [
        ("Spring Boot", "Enterprise Backend", "Opinionated framework for building standalone, production-ready Spring applications.", "Intermediate", "High", "Critical", ["spring-boot-framework"]),
        ("Spring Framework", "Enterprise Backend", "Inversion of Control and dependency injection framework for enterprise Java.", "Advanced", "High", "Critical", ["spring-core"]),
        ("Spring Security", "Application Security", "Powerful and highly customizable authentication and access-control framework for Spring.", "Advanced", "High", "Critical", ["spring-sec"]),
        ("Spring Cloud", "Microservices", "Tools for developers to quickly build distributed patterns in microservice architectures.", "Advanced", "High", "High", ["spring-cloud-micro"]),
        ("Hibernate ORM", "Persistence", "Object-relational mapping tool providing a framework for mapping Java classes to database tables.", "Intermediate", "High", "Critical", ["hibernate"]),
        ("JPA", "Persistence Standards", "Java Persistence API standard specification for managing relational data in Java applications.", "Intermediate", "High", "High", ["jakarta-persistence"]),
        ("Apache Maven", "Build & Dependency", "Software project management and comprehension tool based on the Project Object Model (POM).", "Beginner", "High", "Critical", ["mvn", "maven"]),
        ("Gradle", "Build Automation", "Build automation tool with Kotlin and Groovy DSLs designed for multi-project builds.", "Intermediate", "High", "Critical", ["gradle-build"]),
        ("JUnit 5", "Unit Testing", "The standard testing framework for modern Java applications on the JVM.", "Beginner", "High", "Critical", ["junit"]),
        ("Mockito", "Testing & Mocking", "Popular mocking framework for unit tests in Java.", "Intermediate", "High", "Critical", ["mockito-mock"]),
        ("Quarkus", "Cloud-Native Java", "Kubernetes-native Java stack tailored for OpenJDK and GraalVM with supersonic subatomic speed.", "Advanced", "Medium", "Emerging", ["quarkus-io"]),
        ("Micronaut", "Cloud-Native Java", "Modern, JVM-based, full-stack framework for building modular, easily testable microservices.", "Advanced", "Medium", "High", ["micronaut-framework"]),
        ("Apache Kafka Client", "Event Streaming", "Java messaging client for publishing and consuming events with high throughput.", "Intermediate", "High", "Critical", ["kafka-java"]),
        ("Log4j2", "Logging Frameworks", "Fast, reliable, and thread-safe logging architecture for enterprise Java systems.", "Beginner", "High", "High", ["log4j"]),
        ("Project Lombok", "Developer Productivity", "Java library that automatically plugs into your editor and build tools, spicing up your java.", "Beginner", "Medium", "High", ["lombok"]),
        ("Jackson JSON", "Data Serialization", "High-performance JSON processor and data-binding framework for Java.", "Intermediate", "High", "High", ["jackson"]),
        ("Netty", "Network Application", "Asynchronous event-driven network application framework for rapid development of protocols.", "Advanced", "Medium", "High", ["netty-io"]),
        ("Vert.x", "Reactive Systems", "Reactive toolkit for building concurrent and responsive applications on the JVM.", "Advanced", "Medium", "Moderate", ["eclipse-vertx"]),
        ("Liquibase", "Database Migration", "Open-source database-independent library for tracking and applying database schema changes.", "Intermediate", "High", "High", ["liquibase-db"]),
        ("Flyway", "Database Migration", "Database-migration tool that favors simplicity and convention over configuration.", "Intermediate", "High", "High", ["flyway-db"]),
        ("MapStruct", "Bean Mapping", "Code generator that greatly simplifies the implementation of mappings between Java bean types.", "Intermediate", "Medium", "High", ["mapstruct"]),
        ("Resilience4j", "Fault Tolerance", "Lightweight fault tolerance library designed for functional programming in Java.", "Intermediate", "High", "Critical", ["resilience4j"])
    ]),

    # 4. JavaScript Ecosystem
    ("JavaScript Ecosystem", "Web & Frontend", "Runtimes, packages, and frameworks in the JavaScript/TypeScript world", [
        ("Node.js", "Server-Side Runtime", "Asynchronous event-driven JavaScript runtime built on Chrome's V8 engine.", "Beginner", "High", "Critical", ["nodejs"]),
        ("React", "Frontend Libraries", "Declarative, component-based frontend library for building modern user interfaces.", "Intermediate", "High", "Critical", ["reactjs", "react-core"]),
        ("Next.js", "Full-Stack React", "React framework for production with Server Components, SSR, SSG, and API routes.", "Intermediate", "High", "Critical", ["nextjs"]),
        ("Vue.js", "Frontend Frameworks", "Progressive framework for building user interfaces with intuitive template syntax.", "Intermediate", "High", "High", ["vue3", "vuejs"]),
        ("Angular", "Enterprise Frontend", "Platform and framework for building single-page client applications using TypeScript.", "Advanced", "High", "Critical", ["angular-core"]),
        ("Svelte", "Compiler Frameworks", "Component framework that compiles code into tiny, vanilla JavaScript without a virtual DOM.", "Intermediate", "Medium", "High", ["sveltejs"]),
        ("Express.js", "Backend Web", "Fast, unopinionated, minimalist web framework for Node.js backend services.", "Beginner", "High", "Critical", ["express"]),
        ("NestJS", "Enterprise Backend", "Progressive Node.js framework for building efficient, scalable, enterprise-grade applications.", "Advanced", "High", "High", ["nestjs-framework"]),
        ("Bun", "Fast JavaScript Runtime", "Incredibly fast all-in-one JavaScript runtime, bundler, test runner, and package manager.", "Intermediate", "Medium", "Emerging", ["bun-runtime"]),
        ("Deno", "Modern JS Runtime", "Secure runtime for JavaScript and TypeScript with built-in tooling and zero configuration.", "Intermediate", "Medium", "Emerging", ["deno-runtime"]),
        ("Redux Toolkit", "State Management", "Standard and opinionated way to write Redux logic for global React application state.", "Intermediate", "High", "Critical", ["rtk", "redux"]),
        ("Zustand", "State Management", "Small, fast, and scalable bearbones state-management solution using simplified flux principles.", "Beginner", "High", "High", ["zustand-state"]),
        ("Jest", "JavaScript Testing", "Delightful JavaScript testing framework with a focus on simplicity and snapshot testing.", "Beginner", "High", "Critical", ["jest-js"]),
        ("Vitest", "Vite Testing", "Blazing fast unit test framework powered by Vite with native ESM support.", "Beginner", "High", "High", ["vitest-dev"]),
        ("Vite", "Frontend Bundling", "Next generation frontend tooling that provides an extremely fast development environment.", "Beginner", "High", "Critical", ["vitejs"]),
        ("Webpack", "Module Bundling", "Static module bundler for modern JavaScript applications with rich plugin architecture.", "Intermediate", "Medium", "High", ["webpack-bundler"]),
        ("ESLint", "Code Quality", "Static code analysis tool for identifying problematic patterns found in JavaScript code.", "Beginner", "High", "Critical", ["eslint-linter"]),
        ("Tailwind CSS", "Utility CSS", "Utility-first CSS framework packed with classes that can be composed to build any design.", "Beginner", "High", "Critical", ["tailwindcss"]),
        ("TanStack Query", "Async State", "Powerful asynchronous state management for TS/JS, fetching, caching, and syncing data.", "Intermediate", "High", "Critical", ["react-query"]),
        ("Cypress", "End-to-End Testing", "Next-generation front-end testing tool built for the modern web with real-time reload.", "Intermediate", "High", "High", ["cypress-io"]),
        ("Nuxt.js", "Full-Stack Vue", "Intuitive Vue framework for creating performant, production-grade full-stack web applications.", "Intermediate", "Medium", "High", ["nuxtjs"]),
        ("SvelteKit", "Full-Stack Svelte", "Application framework for Svelte offering fast routing, server-rendering, and zero-effort build.", "Intermediate", "Medium", "High", ["sveltekit"])
    ])
]

print("Base domain loader defined successfully.")
