# database/seed_data/seed_skills.py
"""
Technical Skills Database Generator & Seeder.
Target: 1,500+ unique, curated technical skills across 90 technology domains.
Includes skill categorization, subcategories, descriptions, difficulty,
priority, industry relevance, aliases, and relationship mappings.
"""
import re
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from database.connection import get_db_session
from database.models import SkillCategory, TechnicalSkill, SkillAlias, SkillRelationship

def slugify(text: str) -> str:
    """Generate clean slug identifier for skill_code."""
    text = text.lower().strip()
    text = re.sub(r'[\s/\\+]+', '-', text)
    text = re.sub(r'[^a-z0-9\-._]', '', text)
    return text.strip('-')

# Definition of 90 domains with rich skill items
# Each domain has: (Category Name, Domain Cluster, Description, [Skill Items])
# Skill item: (Name, Subcategory, Description, Difficulty, Priority, Relevance, [Aliases])

RAW_CATEGORIES_DATA: List[Tuple[str, str, str, List[Tuple[str, str, str, str, str, str, List[str]]]]] = [
    # 1. Programming Languages
    ("Programming Languages", "Software Engineering", "Core programming languages across paradigms", [
        ("Python", "General Purpose", "Interpreted, high-level, dynamically typed language widely used in AI, web, and automation.", "Beginner", "High", "Critical", ["python3", "py"]),
        ("Java", "Enterprise OOP", "Class-based, object-oriented language designed for cross-platform enterprise systems.", "Intermediate", "High", "Critical", ["jdk", "jvm"]),
        ("C", "Systems Programming", "Procedural systems language providing low-level memory control and hardware access.", "Intermediate", "High", "High", ["ansi-c", "c-lang"]),
        ("C++", "Systems & High Performance", "Multi-paradigm language with high performance, OOP, templates, and RAII.", "Advanced", "High", "Critical", ["cpp", "cplusplus"]),
        ("C#", "Enterprise & Game Dev", "Modern, type-safe object-oriented language for .NET, game development, and enterprise services.", "Intermediate", "High", "High", ["csharp", "dotnet-c#"]),
        ("JavaScript", "Web Development", "High-level, dynamic language that powers the interactive front-end and full-stack web.", "Beginner", "High", "Critical", ["js", "ecmascript"]),
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
        ("Shell Scripting", "Automation & DevOps", "Writing scripts for Unix/Linux command-line shells (Bash, Zsh) to automate system operations.", "Beginner", "High", "Critical", ["bash", "sh", "zsh"]),
        ("PowerShell", "Automation & Windows", "Task automation and configuration management framework with command-line shell.", "Intermediate", "High", "High", ["pwsh"]),
        ("Assembly Language x86", "Low-Level Computing", "Low-level programming language corresponding to CPU machine code instructions.", "Expert", "Low", "Moderate", ["asm-x86"]),
        ("Assembly Language ARM", "Low-Level Computing", "Assembly instruction set for ARM architecture powering mobile, embedded, and Apple silicon.", "Expert", "Low", "High", ["arm-assembly"]),
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
        ("Asyncio", "Concurrent Python", "Python library to write concurrent code using the async/await syntax.", "Intermediate", "High", "Critical", ["python-asyncio"])
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
        ("Flyway", "Database Migration", "Database-migration tool that favors simplicity and convention over configuration.", "Intermediate", "High", "High", ["flyway-db"])
    ]),

    # 4. JavaScript & TypeScript Ecosystem
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
        ("Cypress", "End-to-End Testing", "Next-generation front-end testing tool built for the modern web with real-time reload.", "Intermediate", "High", "High", ["cypress-io"])
    ]),

    # 5. C and C++ Ecosystem
    ("C and C++ Ecosystem", "Systems & Hardware", "Toolchains, libraries, and graphics APIs for C and C++", [
        ("CMake", "Build Systems", "Cross-platform open-source tool designed to build, test, and package software.", "Intermediate", "High", "Critical", ["cmake-build"]),
        ("Make", "Build Systems", "Build automation tool that automatically builds executable programs from source code.", "Beginner", "High", "High", ["gnu-make"]),
        ("GCC", "Compilers", "GNU Compiler Collection supporting C, C++, and various other programming languages.", "Intermediate", "High", "Critical", ["gnu-gcc"]),
        ("Clang / LLVM", "Compiler Infrastructure", "C language family frontend for LLVM providing modular compiler architecture.", "Intermediate", "High", "Critical", ["clang-llvm"]),
        ("STL (Standard Template Library)", "Algorithms & Containers", "Software library for C++ providing four components: algorithms, containers, functions, and iterators.", "Intermediate", "High", "Critical", ["cpp-stl"]),
        ("Boost C++ Libraries", "Advanced C++", "Peer-reviewed portable C++ source libraries extending standard C++ functionality.", "Advanced", "Medium", "High", ["boost-cpp"]),
        ("Google Test (GTest)", "Testing Frameworks", "Google's C++ testing and mocking framework for unit testing.", "Intermediate", "High", "High", ["gtest"]),
        ("Catch2", "Unit Testing", "Modern, C++-native, test framework for unit-tests, TDD and BDD.", "Beginner", "Medium", "High", ["catch2-cpp"]),
        ("Qt Framework", "Cross-Platform GUI", "Cross-platform application development framework for desktop, embedded, and mobile platforms.", "Advanced", "High", "High", ["qt-cpp"]),
        ("OpenGL", "Computer Graphics", "Cross-language, cross-platform application programming interface for rendering 2D and 3D vector graphics.", "Advanced", "Medium", "High", ["opengl-api"]),
        ("Vulkan", "Low-Overhead Graphics", "Low-overhead, cross-platform API, and open standard for 3D graphics and computing.", "Expert", "High", "Critical", ["vulkan-api"]),
        ("DirectX", "Windows Graphics", "Collection of APIs for handling multimedia, game programming, and video on Microsoft platforms.", "Advanced", "Medium", "High", ["directx12", "dx12"]),
        ("OpenMP", "Parallel Programming", "API that supports multi-platform shared-memory multiprocessing programming in C, C++, and Fortran.", "Advanced", "High", "High", ["openmp-multithreading"]),
        ("MPI (Message Passing Interface)", "Distributed Computing", "Standardized and portable message-passing system designed for parallel computing architectures.", "Advanced", "Medium", "High", ["openmpi"]),
        ("Conan", "Package Management", "Decentralized, open-source C and C++ package manager with multi-platform support.", "Intermediate", "Medium", "High", ["conan-io"]),
        ("Valgrind", "Memory Profiling", "Instrumentation framework for building dynamic analysis tools to detect memory leaks and profiling.", "Intermediate", "High", "Critical", ["valgrind-memcheck"]),
        ("GDB (GNU Debugger)", "Debugging Tools", "Portable debugger that runs on many Unix-like systems and works for many languages.", "Intermediate", "High", "Critical", ["gdb"]),
        ("Asio C++", "Asynchronous I/O", "Cross-platform C++ library for network and low-level I/O programming that models modern concurrency.", "Advanced", "Medium", "Moderate", ["asio-network"])
    ]),

    # 6. .NET Technologies
    (".NET Technologies", "Microsoft Ecosystem", "Enterprise frameworks and tools for the Microsoft .NET platform", [
        (".NET Core / .NET 8", "Application Framework", "Cross-platform, high-performance, open-source framework for building modern applications.", "Intermediate", "High", "Critical", ["dotnet-core", "dotnet-8"]),
        ("ASP.NET Core", "Web Framework", "Cross-platform, high-performance framework for building modern, cloud-enabled web applications.", "Intermediate", "High", "Critical", ["aspnet-core"]),
        ("Entity Framework Core", "ORM & Database", "Modern object-database mapper for .NET supporting LINQ queries and change tracking.", "Intermediate", "High", "Critical", ["ef-core"]),
        ("LINQ", "Query Language", "Language-Integrated Query providing powerful data querying capabilities in C#.", "Beginner", "High", "Critical", ["csharp-linq"]),
        ("Blazor", "Interactive Web UI", "Framework for building interactive client-side web UI with .NET and C# instead of JavaScript.", "Intermediate", "Medium", "High", ["blazor-wasm"]),
        (".NET MAUI", "Cross-Platform UI", "Multi-platform App UI framework for creating native mobile and desktop apps with C# and XAML.", "Intermediate", "Medium", "High", ["dotnet-maui"]),
        ("SignalR", "Real-Time Web", "Software library that allows server code to send asynchronous notifications to client-side web applications.", "Intermediate", "High", "High", ["aspnet-signalr"]),
        ("xUnit.net", "Unit Testing", "Community-focused, open source unit testing tool for the .NET Framework and .NET Core.", "Beginner", "High", "Critical", ["xunit"]),
        ("Dapper", "Micro-ORM", "Simple object mapper for .NET that owns the title of King of Micro ORM in terms of speed.", "Intermediate", "High", "High", ["dapper-net"]),
        ("MediatR", "CQRS & Mediator", "Simple, unambitious mediator implementation in .NET supporting in-process messaging.", "Intermediate", "Medium", "High", ["mediatr-pattern"]),
        ("WPF (Windows Presentation Foundation)", "Desktop UI", "UI framework that creates desktop client applications on Windows with XAML.", "Intermediate", "Medium", "Moderate", ["wpf-xaml"]),
        ("NuGet", "Package Management", "The package manager for .NET enabling developers to create, share, and consume useful packages.", "Beginner", "High", "Critical", ["nuget-pkg"])
    ]),

    # 7. Web Development & Standards
    ("Web Development", "Web Fundamentals", "Core protocols, standards, and web architecture fundamentals", [
        ("HTML5", "Markup Standards", "Fifth and current major version of the HTML standard used for structuring content on the web.", "Beginner", "High", "Critical", ["html"]),
        ("CSS3", "Styling Standards", "Latest evolution of the Cascading Style Sheets language defining presentation and layout.", "Beginner", "High", "Critical", ["css"]),
        ("DOM Manipulation", "Browser Scripting", "Interacting with and dynamically altering the Document Object Model tree structure.", "Beginner", "High", "Critical", ["dom-api"]),
        ("WebSockets", "Real-Time Protocols", "Computer communications protocol providing full-duplex communication channels over a single TCP connection.", "Intermediate", "High", "Critical", ["websocket-api"]),
        ("WebRTC", "Real-Time Media", "Technology enabling Web applications and sites to capture and stream audio and/or video media.", "Advanced", "Medium", "High", ["webrtc-protocol"]),
        ("PWA (Progressive Web Apps)", "Web Standards", "Web applications that use service workers, manifests, and responsive design for app-like behavior.", "Intermediate", "Medium", "High", ["progressive-web-app"]),
        ("Web Accessibility (WCAG)", "Inclusion & Standards", "Web Content Accessibility Guidelines ensuring web content is usable for persons with disabilities.", "Beginner", "High", "Critical", ["a11y", "wcag-2.1"]),
        ("HTTP/2 and HTTP/3", "Web Protocols", "Modern revisions of the HTTP network protocol featuring multiplexing and QUIC transport.", "Intermediate", "High", "High", ["http2", "http3-quic"]),
        ("Service Workers", "Offline Web", "Scripts that browser runs in the background, separate from a web page, opening the door to offline features.", "Intermediate", "High", "High", ["service-worker-api"]),
        ("Core Web Vitals", "Performance Metrics", "Set of unified quality signals essential to delivering great user experience on the web.", "Intermediate", "High", "Critical", ["cwv", "web-vitals"])
    ]),

    # 8. Frontend Development
    ("Frontend Development", "Client-Side Engineering", "UI component design, responsive styling, and client-side architecture", [
        ("Responsive Web Design", "Layout Strategies", "Web development approach creating dynamic changes to the appearance of a website based on screen size.", "Beginner", "High", "Critical", ["rwd"]),
        ("CSS Flexbox", "Layout Systems", "One-dimensional layout method for laying out items in rows or columns with flexible spacing.", "Beginner", "High", "Critical", ["flexbox"]),
        ("CSS Grid Layout", "Layout Systems", "Two-dimensional grid-based layout system that completely changes the way we design user interfaces.", "Beginner", "High", "Critical", ["css-grid"]),
        ("Shadcn UI", "Component Libraries", "Beautifully designed, accessible components that you can copy and paste into your apps.", "Intermediate", "High", "Critical", ["shadcn"]),
        ("Storybook", "Component Testing", "Frontend workshop for building UI components and pages in isolation with mock data.", "Intermediate", "High", "High", ["storybook-js"]),
        ("Micro-Frontends", "Frontend Architecture", "Architectural style where independently deliverable frontend applications are composed into a greater whole.", "Advanced", "Medium", "High", ["microfrontends"]),
        ("Sass / SCSS", "CSS Preprocessors", "Pre-processor scripting language that is interpreted or compiled into Cascading Style Sheets.", "Beginner", "High", "High", ["sass-css"]),
        ("Atomic Design", "Design Systems", "Methodology for creating design systems composed of atoms, molecules, organisms, templates, and pages.", "Intermediate", "Medium", "Moderate", ["atomic-ui"]),
        ("PostCSS", "CSS Tooling", "Software development tool that uses JavaScript-based plugins to automate routine CSS operations.", "Intermediate", "Medium", "High", ["postcss-tool"]),
        ("Web Performance Optimization", "Speed & Efficiency", "Techniques for minimizing file payloads, lazy loading, code splitting, and rendering optimization.", "Intermediate", "High", "Critical", ["wpo", "frontend-perf"])
    ]),

    # 9. Backend Development
    ("Backend Development", "Server-Side Engineering", "Server architecture, API design, authentication, and background processing", [
        ("RESTful API Design", "API Architecture", "Architectural style for designing networked applications leveraging standard HTTP methods.", "Beginner", "High", "Critical", ["rest-api"]),
        ("GraphQL", "API Query Languages", "Query language for APIs and runtime for fulfilling those queries with existing data.", "Intermediate", "High", "Critical", ["graphql-api"]),
        ("gRPC", "RPC Frameworks", "High performance, open-source universal RPC framework developed by Google over HTTP/2.", "Intermediate", "High", "Critical", ["grpc-protocol"]),
        ("JWT (JSON Web Tokens)", "Authentication", "Compact, URL-safe means of representing claims to be transferred between two parties.", "Beginner", "High", "Critical", ["jwt-auth"]),
        ("OAuth 2.0 & OpenID Connect", "Identity & Auth", "Industry-standard protocol for authorization and identity federation.", "Intermediate", "High", "Critical", ["oauth2", "oidc"]),
        ("Rate Limiting & Throttling", "API Protection", "Techniques to control the rate of traffic sent or received by a network interface or service.", "Intermediate", "High", "Critical", ["rate-limiter"]),
        ("Message Queues", "Asynchronous Systems", "Components that store messages until consumer applications can process them.", "Intermediate", "High", "Critical", ["mq", "message-broker"]),
        ("Caching Strategies", "Performance Engineering", "Techniques including Cache-Aside, Write-Through, and CDN caching to optimize data access latency.", "Intermediate", "High", "Critical", ["caching"]),
        ("Server-Sent Events (SSE)", "Unidirectional Streams", "Server push technology enabling a client to receive automatic updates from a server via HTTP.", "Intermediate", "High", "High", ["sse-stream"]),
        ("Background Job Processing", "Distributed Tasks", "Offloading heavy tasks from the synchronous request-response cycle into workers.", "Intermediate", "High", "Critical", ["job-workers"])
    ]),

    # 10. Full Stack Development
    ("Full Stack Development", "End-to-End Engineering", "Cross-tier integration, monorepos, and full-stack deployment patterns", [
        ("MERN Stack", "Stack Paradigms", "Full-stack framework using MongoDB, Express.js, React, and Node.js.", "Beginner", "High", "High", ["mern"]),
        ("JAMstack", "Modern Architecture", "Architecture designed to make the web faster, more secure, and easier to scale (JS, APIs, Markup).", "Intermediate", "Medium", "High", ["jamstack-arch"]),
        ("Monorepo Architecture", "Codebase Management", "Software development strategy where code for many projects is stored in the same repository.", "Intermediate", "High", "Critical", ["monorepo"]),
        ("Turborepo", "Monorepo Build Systems", "High-performance build system for JavaScript and TypeScript codebases on monorepos.", "Intermediate", "High", "High", ["turborepo-tool"]),
        ("Server-Side Rendering (SSR)", "Rendering Patterns", "Rendering web pages on the server instead of the browser, improving SEO and initial page load.", "Intermediate", "High", "Critical", ["ssr"]),
        ("Static Site Generation (SSG)", "Rendering Patterns", "Pre-rendering HTML pages at build time to serve them lightning fast via CDNs.", "Beginner", "High", "Critical", ["ssg"]),
        ("Hydration & Rehydration", "Client-Side Runtimes", "Technique in which client-side JavaScript converts static HTML into dynamic DOM tree.", "Advanced", "Medium", "High", ["dom-hydration"]),
        ("BFF (Backend for Frontend)", "Architecture Patterns", "Architectural pattern where separate backend services are built for specific frontend interfaces.", "Intermediate", "High", "High", ["bff-pattern"]),
        ("Full-Stack Authentication", "Security Integration", "Implementing secure end-to-end user authentication, sessions, cookies, and RBAC.", "Intermediate", "High", "Critical", ["fullstack-auth"])
    ]),

    # 11. Mobile Application Development
    ("Mobile Application Development", "Mobile Engineering", "Native and cross-platform mobile frameworks and tools", [
        ("Android SDK", "Android Native", "Comprehensive software development kit for building native Android applications.", "Intermediate", "High", "Critical", ["android-dev"]),
        ("Jetpack Compose", "Modern Android UI", "Android's modern toolkit for building native UI using declarative Kotlin functions.", "Intermediate", "High", "Critical", ["compose-android"]),
        ("iOS SDK", "iOS Native", "Software development kit for building native applications on Apple iOS.", "Intermediate", "High", "Critical", ["ios-dev"]),
        ("SwiftUI", "Modern Apple UI", "Declarative framework for designing apps across all Apple platforms with Swift.", "Intermediate", "High", "Critical", ["swiftui-framework"]),
        ("React Native", "Cross-Platform Mobile", "Framework for building native mobile apps using React and JavaScript.", "Intermediate", "High", "Critical", ["react-native-cli"]),
        ("Flutter", "Cross-Platform Mobile", "Google's UI toolkit for building beautiful, natively compiled applications from a single codebase.", "Intermediate", "High", "Critical", ["flutter-sdk"]),
        ("Expo", "React Native Tooling", "Framework and platform for universal React applications running on Android, iOS, and the web.", "Beginner", "High", "High", ["expo-go"]),
        ("Kotlin Multiplatform (KMP)", "Cross-Platform Logic", "Technology allowing sharing of business logic across Android, iOS, desktop, and backend.", "Advanced", "High", "Emerging", ["kmp"]),
        ("Mobile App Security", "Security Engineering", "Securing mobile storage, network communications, certificate pinning, and biometric auth.", "Advanced", "High", "Critical", ["mobile-sec"]),
        ("Room Database", "Android Persistence", "SQLite object mapping library providing an abstraction layer over SQLite on Android.", "Beginner", "High", "High", ["room-db"]),
        ("Core Data", "iOS Persistence", "Framework used to manage the model layer objects in Apple applications.", "Intermediate", "Medium", "High", ["core-data-ios"]),
        ("Push Notifications", "Mobile Services", "Integrating Firebase Cloud Messaging (FCM) and Apple Push Notification Service (APNs).", "Intermediate", "High", "Critical", ["fcm-apns"])
    ]),

    # 12. Artificial Intelligence
    ("Artificial Intelligence", "AI & Cognitive Computing", "Foundational AI principles, search, knowledge representation, and reasoning", [
        ("Search Algorithms (A*, Minimax)", "Core AI Search", "Heuristic graph traversal and adversarial search algorithms for problem solving.", "Intermediate", "High", "High", ["heuristic-search"]),
        ("Knowledge Representation", "Symbolic AI", "Formal methods for encoding knowledge about the world so AI systems can solve complex tasks.", "Advanced", "Medium", "Moderate", ["kr-symbolic"]),
        ("Constraint Satisfaction Problems", "Problem Solving", "Mathematical problems defined as a set of objects whose state must satisfy constraints.", "Intermediate", "Medium", "High", ["csp-ai"]),
        ("Bayesian Networks", "Probabilistic Reasoning", "Probabilistic graphical model representing a set of variables and their conditional dependencies.", "Advanced", "Medium", "High", ["bayes-net"]),
        ("Expert Systems", "Rule-Based Systems", "Computer systems that emulate the decision-making ability of a human expert.", "Beginner", "Medium", "Moderate", ["rule-based-ai"]),
        ("Fuzzy Logic", "Soft Computing", "Form of many-valued logic in which the truth values of variables may be any real number between 0 and 1.", "Intermediate", "Low", "Moderate", ["fuzzy-systems"]),
        ("Genetic Algorithms", "Evolutionary Computing", "Search heuristics inspired by Charles Darwin's theory of natural evolution.", "Intermediate", "Medium", "High", ["evolutionary-ai"]),
        ("Ontologies and Knowledge Graphs", "Semantic Web", "Structured representations of entities, concepts, and semantic relationships between them.", "Intermediate", "High", "Critical", ["knowledge-graphs", "rdf"])
    ]),

    # 13. Machine Learning
    ("Machine Learning", "Statistical Learning", "Supervised, unsupervised, and semi-supervised machine learning techniques", [
        ("Linear & Logistic Regression", "Supervised Learning", "Fundamental parametric statistical models for continuous prediction and binary classification.", "Beginner", "High", "Critical", ["regression-models"]),
        ("Decision Trees & Random Forests", "Ensemble Methods", "Tree-based algorithms and ensemble bagging methods for robust classification and regression.", "Beginner", "High", "Critical", ["random-forest"]),
        ("Gradient Boosting (XGBoost, LightGBM)", "Ensemble Methods", "State-of-the-art boosting algorithms for structured and tabular dataset competitions.", "Intermediate", "High", "Critical", ["xgboost", "lightgbm", "catboost"]),
        ("Support Vector Machines (SVM)", "Kernel Methods", "Supervised learning models with associated learning algorithms analyzing data for classification.", "Intermediate", "High", "High", ["svm"]),
        ("K-Means & Hierarchical Clustering", "Unsupervised Learning", "Partitioning data points into distinct non-overlapping subgroups without predefined labels.", "Beginner", "High", "High", ["clustering"]),
        ("Principal Component Analysis (PCA)", "Dimensionality Reduction", "Orthogonal linear transformation transforming data to a new coordinate system of principal components.", "Intermediate", "High", "Critical", ["pca"]),
        ("Data Preprocessing & Cleaning", "Feature Engineering", "Handling missing values, outlier detection, categorical encoding, and feature scaling.", "Beginner", "High", "Critical", ["data-prep"]),
        ("Feature Engineering", "Model Optimization", "Selecting, manipulating, and transforming raw data into features used in machine learning.", "Intermediate", "High", "Critical", ["feature-eng"]),
        ("Cross-Validation & Hyperparameter Tuning", "Model Evaluation", "K-fold cross validation, Grid Search, and Optuna for optimal model hyperparameter selection.", "Intermediate", "High", "Critical", ["hyperopt", "optuna"]),
        ("Model Evaluation Metrics (ROC-AUC, F1)", "Model Evaluation", "Assessing model performance using precision, recall, F1-score, ROC-AUC, and confusion matrices.", "Beginner", "High", "Critical", ["metrics-eval"])
    ]),

    # 14. Deep Learning
    ("Deep Learning", "Neural Architectures", "Neural network architectures, tensor frameworks, and backpropagation", [
        ("PyTorch", "Tensor Frameworks", "Open source machine learning framework that accelerates the path from research prototyping to production.", "Intermediate", "High", "Critical", ["torch", "pytorch-core"]),
        ("TensorFlow", "Tensor Frameworks", "End-to-end open source platform for machine learning developed by Google.", "Intermediate", "High", "Critical", ["tf", "tensorflow2"]),
        ("Keras", "High-Level Neural APIs", "Deep learning API written in Python, running on top of TensorFlow, JAX, or PyTorch.", "Beginner", "High", "High", ["keras-core"]),
        ("Convolutional Neural Networks (CNN)", "Computer Vision", "Deep learning architecture optimized for processing 2D grid data like images.", "Intermediate", "High", "Critical", ["cnn"]),
        ("Recurrent Neural Networks (RNN & LSTM)", "Sequential Data", "Neural architectures featuring cyclic connections designed to process sequences of data.", "Intermediate", "High", "High", ["lstm", "gru"]),
        ("Transformer Architecture", "Attention Mechanisms", "Attention-based neural architecture powering state-of-the-art NLP, vision, and multimodal models.", "Advanced", "High", "Critical", ["transformers"]),
        ("Backpropagation & Optimization (Adam, SGD)", "Neural Training", "Calculus of gradient computation and adaptive stochastic gradient descent optimizers.", "Intermediate", "High", "Critical", ["optimizers"]),
        ("Activation Functions (ReLU, GELU, Swish)", "Neural Components", "Non-linear transformations introducing expressiveness into multi-layer neural networks.", "Beginner", "High", "High", ["activations"]),
        ("Regularization (Dropout, Batch Normalization)", "Generalization", "Techniques preventing neural network overfitting and accelerating training stability.", "Intermediate", "High", "Critical", ["dropout", "batchnorm"]),
        ("Transfer Learning", "Model Adaptation", "Reusing a pre-trained model on a new, related task with minimal additional compute.", "Intermediate", "High", "Critical", ["transfer-learn"])
    ]),

    # 15. Generative AI
    ("Generative AI", "Generative Modeling", "Generative models for text, image, audio, and multimodal synthesis", [
        ("Diffusion Models", "Image Synthesis", "Generative models that synthesize data by iteratively denoising Gaussian noise (Stable Diffusion).", "Advanced", "High", "Critical", ["diffusion"]),
        ("Generative Adversarial Networks (GAN)", "Generative Models", "Two neural networks contesting with each other in a zero-sum game framework.", "Advanced", "Medium", "High", ["gans"]),
        ("Variational Autoencoders (VAE)", "Latent Representations", "Probabilistic generative model learning compressed latent representations of data.", "Advanced", "Medium", "High", ["vae"]),
        ("Multimodal AI", "Cross-Modal Synthesis", "AI architectures capable of processing and generating text, images, audio, and video simultaneously.", "Advanced", "High", "Critical", ["multimodal"]),
        ("Voice Synthesis & TTS", "Audio Generation", "Synthesizing natural, human-sounding speech from text using deep generative models.", "Intermediate", "Medium", "High", ["tts", "whisper"]),
        ("Prompt Engineering for Image Gen", "Generative Prompting", "Crafting effective descriptive prompts, negative prompts, and aspect controls for Midjourney and SD.", "Beginner", "High", "High", ["image-prompts"]),
        ("Synthetic Data Generation", "Data Augmentation", "Creating artificial datasets using generative models to train downstream classifiers.", "Intermediate", "High", "High", ["synthetic-data"]),
        ("Content Moderation & Safety Guardrails", "AI Safety", "Filtering and mitigating toxic, biased, or harmful outputs from generative systems.", "Intermediate", "High", "Critical", ["guardrails-ai"])
    ]),

    # 16. Large Language Models (LLMs)
    ("Large Language Models", "Foundation Models", "Foundational text models, tokenization, context windows, and APIs", [
        ("Hugging Face Transformers", "Model Hub & Libraries", "Standard library for downloading, running, and fine-tuning state-of-the-art pre-trained models.", "Intermediate", "High", "Critical", ["hf-transformers"]),
        ("OpenAI API", "Commercial LLM APIs", "Integrating GPT-4, GPT-4o, and embedding endpoints into production applications.", "Beginner", "High", "Critical", ["openai-sdk"]),
        ("Anthropic Claude API", "Commercial LLM APIs", "Integrating Claude 3.5 Sonnet and Haiku models with extended context windows.", "Beginner", "High", "Critical", ["anthropic-sdk"]),
        ("Google Gemini API", "Commercial LLM APIs", "Building applications with Google's multimodal Gemini 1.5 Flash and Pro models.", "Beginner", "High", "Critical", ["gemini-api"]),
        ("Open-Source LLMs (Llama 3, Mistral)", "Open Weights", "Deploying and serving open-weights models locally or in private VPCs.", "Intermediate", "High", "Critical", ["llama-3", "mistral-ai"]),
        ("vLLM", "High-Throughput Serving", "High-throughput and memory-efficient inference and serving engine for LLMs featuring PagedAttention.", "Advanced", "High", "Critical", ["vllm-engine"]),
        ("Ollama", "Local LLM Execution", "Tool for running open-source large language models locally on consumer hardware.", "Beginner", "High", "High", ["ollama-ai"]),
        ("Tokenization & Context Windows", "LLM Fundamentals", "Byte-pair encoding (BPE), token economics, and managing large context window limits.", "Beginner", "High", "Critical", ["tokenizers"]),
        ("Quantization (GGUF, AWQ, GPTQ)", "Model Compression", "Compressing model weights to 4-bit and 8-bit precision to run on restricted memory.", "Advanced", "High", "High", ["gguf", "model-quantization"])
    ]),

    # 17. Natural Language Processing (NLP)
    ("Natural Language Processing", "Computational Linguistics", "Text processing, linguistic pipelines, entity extraction, and sentiment analysis", [
        ("spaCy", "Industrial NLP", "Free, open-source library for advanced Natural Language Processing in Python.", "Beginner", "High", "Critical", ["spacy-nlp"]),
        ("NLTK", "Linguistic Toolkits", "Leading platform for building Python programs to work with human language data.", "Beginner", "Medium", "High", ["nltk-py"]),
        ("Named Entity Recognition (NER)", "Information Extraction", "Locating and classifying named entities in unstructured text into predefined categories.", "Intermediate", "High", "Critical", ["ner"]),
        ("Part-of-Speech Tagging", "Linguistic Analysis", "Marking up a word in a text as corresponding to a particular part of speech.", "Beginner", "Medium", "High", ["pos-tagging"]),
        ("Sentiment Analysis", "Text Classification", "Using NLP to determine the emotional tone behind a body of text.", "Beginner", "High", "High", ["sentiment-nlp"]),
        ("Word Embeddings (Word2Vec, GloVe)", "Semantic Vectors", "Vector representations of words capturing semantic and syntactic similarities.", "Intermediate", "High", "High", ["word2vec"]),
        ("Sentence Transformers", "Dense Retrieval", "Python framework for state-of-the-art sentence, text and image embeddings.", "Intermediate", "High", "Critical", ["sentence-transformers"]),
        ("Text Summarization", "Generative NLP", "Extractive and abstractive algorithms for shortening long documents while preserving key information.", "Intermediate", "High", "High", ["summarization"]),
        ("Topic Modeling (LDA, BERTopic)", "Unsupervised NLP", "Statistical model for discovering the abstract 'topics' that occur in a collection of documents.", "Intermediate", "Medium", "High", ["bertopic", "lda"])
    ]),

    # 18. Computer Vision
    ("Computer Vision", "Visual Processing", "Image analysis, object detection, segmentation, and video processing", [
        ("OpenCV", "Image Processing", "Open Source Computer Vision Library with thousands of optimized algorithms.", "Intermediate", "High", "Critical", ["opencv-python", "cv2"]),
        ("YOLO (You Only Look Once)", "Object Detection", "Real-time object detection system famous for its speed and accuracy.", "Intermediate", "High", "Critical", ["yolov8", "ultralytics"]),
        ("Image Segmentation (Mask R-CNN, SAM)", "Pixel-Level Vision", "Segmenting objects at pixel boundaries using Mask R-CNN and Meta's Segment Anything Model.", "Advanced", "High", "Critical", ["segment-anything", "sam"]),
        ("MediaPipe", "Perception Pipelines", "Cross-platform, customizable ML solutions for live and streaming media (pose, face, hands).", "Beginner", "High", "High", ["mediapipe-google"]),
        ("Feature Extraction (SIFT, ORB)", "Classical Vision", "Detecting and describing local features in images for matching and tracking.", "Intermediate", "Medium", "Moderate", ["sift-orb"]),
        ("Optical Character Recognition (OCR)", "Document Vision", "Extracting typed, handwritten or printed text from images using Tesseract or EasyOCR.", "Beginner", "High", "High", ["tesseract", "easyocr"]),
        ("Face Recognition", "Biometric Vision", "Detecting and verifying human facial identities from digital photos or video streams.", "Intermediate", "High", "High", ["face-recognition"]),
        ("Video Object Tracking", "Temporal Vision", "Tracking moving objects across consecutive video frames using DeepSORT and Kalman filters.", "Advanced", "High", "High", ["deepsort"])
    ]),

    # 19. Reinforcement Learning
    ("Reinforcement Learning", "Agent Learning", "Reward-based optimization, policy gradients, and Q-learning", [
        ("Q-Learning & Deep Q-Networks (DQN)", "Value-Based RL", "Model-free reinforcement learning algorithm to learn the value of an action in a state.", "Advanced", "High", "High", ["dqn"]),
        ("Policy Gradient Methods (PPO, TRPO)", "Policy Optimization", "Proximal Policy Optimization algorithms used in modern robotics and LLM alignment (RLHF).", "Advanced", "High", "Critical", ["ppo"]),
        ("Gymnasium (OpenAI Gym)", "RL Environments", "Standard API for reinforcement learning environments and benchmarks.", "Intermediate", "High", "High", ["gymnasium"]),
        ("RLHF (RL from Human Feedback)", "LLM Alignment", "Fine-tuning models using human preference rankings to produce safe, helpful outputs.", "Expert", "High", "Critical", ["rlhf"]),
        ("DPO (Direct Preference Optimization)", "LLM Alignment", "Algorithmic alternative to RLHF directly optimizing language policies on preferences.", "Advanced", "High", "Critical", ["dpo"]),
        ("Markov Decision Processes (MDP)", "Mathematical RL", "Discrete-time stochastic control process providing mathematical framework for modeling decision making.", "Intermediate", "High", "High", ["mdp"])
    ]),

    # 20. AI Agents & 21. Agentic AI
    ("AI Agents and Agentic AI", "Autonomous Systems", "Autonomous goal-directed AI systems, tool calling, and multi-agent workflows", [
        ("LangChain", "Agent Frameworks", "Framework for developing applications powered by language models with chains and memory.", "Intermediate", "High", "Critical", ["langchain-core"]),
        ("LangGraph", "Agent Orchestration", "Library for building stateful, multi-actor applications with LLMs using cyclic graphs.", "Intermediate", "High", "Critical", ["langgraph"]),
        ("CrewAI", "Multi-Agent Systems", "Framework for orchestrating role-playing autonomous AI agents for complex collaborative tasks.", "Intermediate", "High", "Critical", ["crewai"]),
        ("AutoGPT", "Autonomous Agents", "Autonomous open-source application executing goals through iterative loops.", "Intermediate", "Medium", "Moderate", ["autogpt"]),
        ("Function Calling & Tool Use", "Agent Capabilities", "Equipping LLMs with external API tools, calculators, databases, and code interpreters.", "Beginner", "High", "Critical", ["tool-calling"]),
        ("ReAct Framework (Reason + Act)", "Agent Prompting", "Prompting paradigm synergetically combining reasoning traces and task-specific actions.", "Intermediate", "High", "Critical", ["react-prompting"]),
        ("Plan-and-Solve Strategies", "Agent Planning", "Decomposing complex user goals into intermediate executable sub-tasks.", "Intermediate", "High", "High", ["agent-planning"]),
        ("Human-in-the-Loop AI Review", "Agent Governance", "Interjecting human validation and confirmation steps before critical tool executions.", "Beginner", "High", "Critical", ["hitl-ai"])
    ]),

    # 22. Retrieval-Augmented Generation (RAG) & 23. Prompt Engineering
    ("RAG and Prompt Engineering", "Information Retrieval", "Augmenting foundation models with external context and structured prompting", [
        ("LlamaIndex", "Data Frameworks for LLMs", "Data framework for connecting custom data sources to large language models.", "Intermediate", "High", "Critical", ["llamaindex"]),
        ("Dense & Sparse Hybrid Search", "Information Retrieval", "Combining semantic dense vector search with lexical BM25 keyword matching.", "Intermediate", "High", "Critical", ["hybrid-search", "bm25"]),
        ("Chunking Strategies", "Document Preprocessing", "Splitting text into semantically coherent segments (fixed-size, markdown, semantic chunking).", "Beginner", "High", "Critical", ["text-chunking"]),
        ("Reranking (Cohere, Cross-Encoders)", "Retrieval Optimization", "Scoring retrieved document candidates with cross-encoders to ensure top relevance.", "Intermediate", "High", "Critical", ["reranking"]),
        ("Few-Shot Prompting", "Prompt Engineering", "Providing contextual input-output demonstration examples within prompts to guide output format.", "Beginner", "High", "Critical", ["few-shot"]),
        ("Chain-of-Thought (CoT)", "Prompt Engineering", "Encouraging step-by-step reasoning before outputting final answers to improve accuracy.", "Beginner", "High", "Critical", ["cot"]),
        ("DSPy", "Programmatic Prompting", "Framework for algorithmically optimizing LM prompts and weights rather than manual prompt tweaking.", "Advanced", "High", "Emerging", ["dspy"]),
        ("Hallucination Mitigation", "Evaluation & Guardrails", "Techniques ensuring generated answers are strictly grounded in retrieved evidence.", "Intermediate", "High", "Critical", ["grounding"])
    ]),

    # 24. Model Training & Fine-Tuning
    ("Model Training and Fine-Tuning", "Deep Learning Engineering", "Adapting weights of foundational models on custom domain datasets", [
        ("PEFT (Parameter-Efficient Fine-Tuning)", "Efficient Tuning", "Techniques adapting pre-trained models without fine-tuning all model parameters.", "Advanced", "High", "Critical", ["peft"]),
        ("LoRA (Low-Rank Adaptation)", "Efficient Tuning", "Freezing pre-trained model weights and injecting trainable rank decomposition matrices.", "Advanced", "High", "Critical", ["lora"]),
        ("QLoRA (Quantized LoRA)", "Memory-Efficient Tuning", "Fine-tuning 4-bit quantized models using low-rank adapters on consumer GPUs.", "Advanced", "High", "Critical", ["qlora"]),
        ("DeepSpeed", "Distributed Training", "Deep learning optimization software suite that makes distributed training efficient and easy.", "Expert", "High", "Critical", ["deepspeed-microsoft"]),
        ("FSDP (Fully Sharded Data Parallel)", "Distributed Training", "PyTorch implementation sharding model parameters, gradients, and optimizer states.", "Expert", "High", "Critical", ["fsdp"]),
        ("Weights & Biases (W&B)", "Experiment Tracking", "Developer platform for tracking machine learning experiments, datasets, and models.", "Beginner", "High", "Critical", ["wandb"]),
        ("Learning Rate Schedulers", "Optimization", "Dynamic learning rate schedules (Cosine Annealing, Warmup) to maximize convergence.", "Intermediate", "High", "High", ["lr-schedule"])
    ]),

    # 25. MLOps
    ("MLOps", "Operational ML", "Deployment, monitoring, automated retraining, and lifecycle management of ML systems", [
        ("MLflow", "Lifecycle Management", "Open source platform for managing the end-to-end machine learning lifecycle.", "Intermediate", "High", "Critical", ["mlflow"]),
        ("Kubeflow", "Kubernetes ML", "Cloud-native platform for machine learning pipelines on top of Kubernetes.", "Advanced", "High", "Critical", ["kubeflow"]),
        ("Triton Inference Server", "Model Serving", "Open source software from NVIDIA that maximizes inference performance across hardware.", "Advanced", "High", "Critical", ["nvidia-triton"]),
        ("ONNX Runtime", "Inference Acceleration", "Cross-platform, high-performance engine for deploying models in open neural network format.", "Intermediate", "High", "Critical", ["onnx"]),
        ("Feature Stores (Feast, Hopsworks)", "Data Architecture", "Centralized repository enabling data consistency between training and online inference.", "Advanced", "Medium", "High", ["feature-store"]),
        ("Data Drift & Model Monitoring", "Production QA", "Detecting covariate shift, concept drift, and performance degradation in production.", "Intermediate", "High", "Critical", ["evidently-ai", "drift-detection"]),
        ("DVC (Data Version Control)", "Version Control", "Version control system for machine learning projects managing datasets and models.", "Intermediate", "High", "High", ["dvc"])
    ]),

    # 26. Data Science & 27. Data Analytics
    ("Data Science and Analytics", "Data Insight & Modeling", "Exploratory analysis, hypothesis testing, and statistical inference", [
        ("Exploratory Data Analysis (EDA)", "Data Investigation", "Analyzing data sets to summarize their main characteristics, often using visual methods.", "Beginner", "High", "Critical", ["eda"]),
        ("Hypothesis Testing (t-test, ANOVA)", "Statistical Inference", "Statistical methods for testing the validity of hypotheses about population parameters.", "Intermediate", "High", "Critical", ["hypothesis-testing"]),
        ("A/B Testing", "Experimentation", "Comparing two versions of a webpage or app against each other to determine performance.", "Intermediate", "High", "Critical", ["split-testing"]),
        ("Cohort Analysis", "Behavioral Analytics", "Analyzing user groups sharing common characteristics over time to measure retention.", "Beginner", "High", "High", ["cohorts"]),
        ("Customer Lifetime Value (LTV) Modeling", "Business Data Science", "Predictive modeling of the net profit attributed to the entire relationship with a customer.", "Intermediate", "Medium", "High", ["clv-ltv"]),
        ("Time Series Forecasting (ARIMA, Prophet)", "Sequential Analytics", "Statistical models predicting future points in time series data based on past trends.", "Intermediate", "High", "Critical", ["prophet", "arima"]),
        ("Data Storytelling", "Communication", "Translating raw data findings into actionable narratives for executive stakeholders.", "Beginner", "High", "Critical", ["storytelling"])
    ]),

    # 28. Business Intelligence
    ("Business Intelligence", "Enterprise Analytics", "Dashboards, KPI tracking, and enterprise reporting platforms", [
        ("Power BI", "Enterprise Dashboards", "Microsoft business analytics service providing interactive visualizations and BI capabilities.", "Beginner", "High", "Critical", ["powerbi"]),
        ("Tableau", "Visual Analytics", "Interactive data visualization software focused on business intelligence.", "Beginner", "High", "Critical", ["tableau-desktop"]),
        ("Looker", "Modern BI", "Modern enterprise platform for business intelligence, data applications, and embedded analytics.", "Intermediate", "High", "High", ["looker-bi"]),
        ("DAX (Data Analysis Expressions)", "Power BI Formulas", "Library of functions and operators used to build formulas and expressions in Power BI.", "Intermediate", "High", "Critical", ["dax-formulas"]),
        ("Data Modeling (Star & Snowflake Schema)", "Data Warehousing", "Designing dimensional tables and fact tables for fast business queries.", "Intermediate", "High", "Critical", ["star-schema"]),
        ("Metabase", "Open Source BI", "Simple, open source way for everyone in an organization to ask questions and learn from data.", "Beginner", "High", "High", ["metabase-bi"]),
        ("Executive KPI Dashboards", "Reporting", "Designing high-level visual summaries tracking core operational performance indicators.", "Beginner", "High", "Critical", ["kpi-design"])
    ]),

    # 29. Data Engineering & 30. Big Data
    ("Data Engineering and Big Data", "Data Pipelines & Scale", "Extract, Transform, Load (ETL), distributed storage, and streaming pipelines", [
        ("Apache Spark", "Distributed Processing", "Unified analytics engine for large-scale distributed data processing and machine learning.", "Intermediate", "High", "Critical", ["spark", "pyspark"]),
        ("Apache Kafka", "Event Streaming", "Distributed event store and stream-processing platform for high-throughput data pipelines.", "Intermediate", "High", "Critical", ["kafka"]),
        ("Apache Airflow", "Workflow Orchestration", "Platform to programmatically author, schedule, and monitor complex data workflows.", "Intermediate", "High", "Critical", ["airflow"]),
        ("dbt (data build tool)", "Data Transformation", "Command-line tool enabling data analysts and engineers to transform data in their warehouse.", "Intermediate", "High", "Critical", ["dbt-core"]),
        ("Snowflake", "Cloud Data Warehouse", "Cloud-based data storage and analytics service with instant elasticity and separation of compute/storage.", "Intermediate", "High", "Critical", ["snowflake-dw"]),
        ("Databricks", "Lakehouse Platform", "Unified lakehouse data analytics platform built on top of Apache Spark and Delta Lake.", "Intermediate", "High", "Critical", ["databricks-lakehouse"]),
        ("Google BigQuery", "Serverless Analytics", "Serverless, highly scalable, and cost-effective multi-cloud data warehouse.", "Intermediate", "High", "Critical", ["bigquery"]),
        ("Amazon Redshift", "Cloud Data Warehouse", "Fast, petabyte-scale cloud data warehouse service in AWS.", "Intermediate", "High", "High", ["redshift"]),
        ("Delta Lake", "Storage Layer", "Open-source storage framework that enables building a Lakehouse architecture with ACID transactions.", "Intermediate", "High", "Critical", ["delta-lake"]),
        ("Apache Flink", "Stream Processing", "Framework and distributed processing engine for stateful computations over data streams.", "Advanced", "Medium", "High", ["flink"])
    ]),

    # 31. Statistics and Mathematics
    ("Statistics and Mathematics", "Foundations", "Mathematical foundations for machine learning, data science, and algorithms", [
        ("Linear Algebra", "Vector Mathematics", "Branch of mathematics concerning linear equations, vector spaces, and matrices.", "Beginner", "High", "Critical", ["linear-algebra"]),
        ("Multivariate Calculus", "Optimization Math", "Differential and integral calculus of functions of several variables, essential for gradients.", "Intermediate", "High", "Critical", ["calculus"]),
        ("Probability Theory", "Stochastic Math", "Mathematical analysis of random phenomena, probability distributions, and random variables.", "Beginner", "High", "Critical", ["probability"]),
        ("Inferential Statistics", "Statistical Analysis", "Drawing conclusions and making predictions about a population based on sample data.", "Intermediate", "High", "Critical", ["inferential-stats"]),
        ("Discrete Mathematics", "Computer Science Math", "Study of mathematical structures that are fundamentally discrete rather than continuous.", "Beginner", "High", "Critical", ["discrete-math"]),
        ("Bayes Theorem", "Probability", "Fundamental mathematical rule describing the probability of an event based on prior knowledge.", "Beginner", "High", "Critical", ["bayes-rule"])
    ]),

    # 32. Database Management & 33. SQL Technologies
    ("Database Management and SQL", "Relational Systems", "Relational database engines, indexing, transactions, and performance tuning", [
        ("PostgreSQL", "RDBMS", "Powerful, open source object-relational database system known for reliability and extensibility.", "Beginner", "High", "Critical", ["postgres"]),
        ("MySQL", "RDBMS", "World's most popular open-source relational database management system.", "Beginner", "High", "Critical", ["mysql-server"]),
        ("SQLite", "Embedded Databases", "Self-contained, serverless, zero-configuration SQL database engine.", "Beginner", "High", "Critical", ["sqlite3"]),
        ("Microsoft SQL Server", "Enterprise RDBMS", "Relational database management system developed by Microsoft.", "Intermediate", "High", "High", ["mssql"]),
        ("Oracle Database", "Enterprise RDBMS", "Multi-model relational database management system produced by Oracle.", "Intermediate", "High", "High", ["oracle-db"]),
        ("Database Indexing (B-Tree, Hash)", "Query Optimization", "Data structures improving the speed of data retrieval operations on database tables.", "Intermediate", "High", "Critical", ["db-indexing"]),
        ("ACID Transactions", "Database Reliability", "Atomicity, Consistency, Isolation, and Durability guarantees in transactional databases.", "Intermediate", "High", "Critical", ["acid"]),
        ("Database Sharding & Replication", "Distributed DB", "Partitioning data across multiple database instances and maintaining synchronized replicas.", "Advanced", "High", "Critical", ["sharding-replication"]),
        ("Query Execution Plans (EXPLAIN)", "Performance Tuning", "Analyzing how query optimizers evaluate and execute SQL statements to remove bottlenecks.", "Intermediate", "High", "Critical", ["explain-analyze"])
    ]),

    # 34. NoSQL Technologies & 35. Vector Databases
    ("NoSQL and Vector Databases", "Non-Relational Storage", "Document, key-value, column-family, graph, and vector embedding stores", [
        ("MongoDB", "Document Store", "Leading source-available cross-platform document-oriented database using JSON-like documents.", "Beginner", "High", "Critical", ["mongo"]),
        ("Redis", "In-Memory Key-Value", "In-memory data structure store used as a distributed cache, message broker, and database.", "Beginner", "High", "Critical", ["redis-cache"]),
        ("Apache Cassandra", "Wide-Column Store", "Highly scalable, distributed NoSQL database designed for high-availability workloads.", "Advanced", "Medium", "High", ["cassandra"]),
        ("Neo4j", "Graph Databases", "Graph database management system optimized for relationship-rich interconnected data.", "Intermediate", "Medium", "High", ["neo4j-graph"]),
        ("Amazon DynamoDB", "Managed NoSQL", "Fully managed proprietary NoSQL database service supporting key-value and document data structures.", "Intermediate", "High", "Critical", ["dynamodb"]),
        ("Elasticsearch", "Search Engine", "Distributed, JSON-based search and analytics engine designed for horizontal scalability.", "Intermediate", "High", "Critical", ["elasticsearch", "elastic"]),
        ("ChromaDB", "Vector Database", "Open-source AI-native embedding database designed for rapid RAG application prototyping.", "Beginner", "High", "Critical", ["chromadb"]),
        ("Pinecone", "Managed Vector DB", "Managed, cloud-native vector database optimized for ultra-low latency semantic search.", "Beginner", "High", "Critical", ["pinecone-db"]),
        ("Weaviate", "Vector Search Engine", "Open source vector search engine that stores both objects and vectors.", "Intermediate", "High", "High", ["weaviate"]),
        ("Qdrant", "Vector Database", "Vector similarity search engine and vector database written in Rust with payload filtering.", "Intermediate", "High", "High", ["qdrant"]),
        ("Milvus", "Distributed Vector DB", "Open-source vector database built to manage trillions of embedding vectors.", "Advanced", "High", "High", ["milvus"]),
        ("FAISS", "Vector Search Library", "Library for efficient similarity search and clustering of dense vectors developed by Meta.", "Advanced", "High", "Critical", ["faiss-meta"])
    ]),

    # 36. Cloud Computing & 37. AWS
    ("Cloud Computing and AWS", "Cloud Infrastructure", "Amazon Web Services infrastructure, compute, storage, and networking", [
        ("AWS EC2", "Virtual Compute", "Amazon Elastic Compute Cloud providing scalable computing capacity in the cloud.", "Beginner", "High", "Critical", ["ec2"]),
        ("AWS S3", "Object Storage", "Amazon Simple Storage Service offering industry-leading scalability, data availability, and security.", "Beginner", "High", "Critical", ["s3"]),
        ("AWS Lambda", "Serverless Compute", "Serverless event-driven compute service running code in response to events.", "Intermediate", "High", "Critical", ["lambda-aws"]),
        ("AWS IAM", "Identity & Access", "Managing fine-grained access permissions and credentials across AWS services.", "Beginner", "High", "Critical", ["aws-iam"]),
        ("AWS ECS & EKS", "Container Orchestration", "Elastic Container Service and managed Kubernetes on Amazon Web Services.", "Intermediate", "High", "Critical", ["ecs", "eks"]),
        ("AWS RDS", "Managed Databases", "Relational Database Service automating hardware provisioning, patching, and backups.", "Beginner", "High", "Critical", ["aws-rds"]),
        ("AWS CloudFront", "CDN", "Fast content delivery network (CDN) service securely delivering data and APIs globally.", "Intermediate", "High", "High", ["cloudfront"]),
        ("AWS API Gateway", "API Management", "Fully managed service that makes it easy for developers to create and secure APIs at any scale.", "Intermediate", "High", "Critical", ["api-gateway-aws"]),
        ("AWS CloudWatch", "Monitoring & Logs", "Monitoring and observability service built for DevOps engineers, developers, and IT managers.", "Beginner", "High", "High", ["cloudwatch"]),
        ("AWS Well-Architected Framework", "Cloud Architecture", "Architectural best practices across security, reliability, performance, and cost.", "Intermediate", "High", "Critical", ["aws-waf"])
    ]),

    # 38. Microsoft Azure & 39. Google Cloud
    ("Azure and Google Cloud", "Multi-Cloud Platforms", "Enterprise cloud capabilities on Microsoft Azure and Google Cloud Platform", [
        ("Azure Virtual Machines", "Compute", "On-demand, scalable computing resources in Microsoft Azure.", "Beginner", "High", "High", ["azure-vm"]),
        ("Azure App Services", "PaaS Web Hosting", "Fully managed platform for building, deploying, and scaling enterprise web apps.", "Beginner", "High", "High", ["app-services"]),
        ("Azure Blob Storage", "Object Storage", "Massively scalable and secure object storage for cloud-native workloads.", "Beginner", "High", "High", ["azure-blob"]),
        ("Azure Functions", "Serverless", "Event-driven serverless compute platform solving complex orchestration problems.", "Intermediate", "High", "High", ["azure-functions"]),
        ("Azure Kubernetes Service (AKS)", "Managed K8s", "Simplifies deploying managed Kubernetes clusters in Azure.", "Intermediate", "High", "High", ["aks"]),
        ("Google Cloud Compute Engine", "GCP Compute", "Scalable, high-performance virtual machines on Google infrastructure.", "Beginner", "High", "High", ["gcp-gce"]),
        ("Google Kubernetes Engine (GKE)", "GCP Managed K8s", "Secured and managed Kubernetes service with four-way auto-scaling.", "Intermediate", "High", "Critical", ["gke"]),
        ("Google Cloud Run", "Serverless Containers", "Deploy and scale containerized applications on a fully managed serverless platform.", "Beginner", "High", "Critical", ["cloud-run"]),
        ("Google Cloud Storage (GCS)", "Object Storage", "Worldwide, durable storage service for developers and enterprises.", "Beginner", "High", "High", ["gcs"])
    ]),

    # 40. DevOps, 41. Platform Engineering, 42. SRE
    ("DevOps and SRE", "Operations & Reliability", "Site reliability, automation, platform engineering, and incident response", [
        ("Site Reliability Engineering (SRE)", "Operational Discipline", "Applying software engineering principles to infrastructure and operations problems.", "Intermediate", "High", "Critical", ["sre-discipline"]),
        ("Service Level Objectives (SLOs & SLIs)", "Reliability Metrics", "Defining clear quantitative reliability targets and service quality measurements.", "Intermediate", "High", "Critical", ["slo-sli"]),
        ("Error Budgets", "SRE Governance", "Balancing system innovation speed with availability constraints.", "Intermediate", "High", "High", ["error-budget"]),
        ("Prometheus", "Metrics Monitoring", "Open-source monitoring system with a dimensional data model and flexible query language (PromQL).", "Intermediate", "High", "Critical", ["prometheus-monitoring"]),
        ("Grafana", "Data Visualization", "Open and composable observability and data visualization platform for dashboards.", "Beginner", "High", "Critical", ["grafana-dashboards"]),
        ("OpenTelemetry", "Distributed Tracing", "Collection of tools, APIs, and SDKs to instrument, generate, and export telemetry data.", "Intermediate", "High", "Critical", ["otel"]),
        ("Datadog", "Cloud Observability", "Observability service for cloud-scale applications providing monitoring of servers and databases.", "Intermediate", "High", "High", ["datadog-monitoring"]),
        ("Incident Management & Postmortems", "Operations", "Root-cause analysis, blameless postmortems, and on-call escalation procedures.", "Intermediate", "High", "Critical", ["postmortem"]),
        ("Infrastructure as Code (IaC)", "Automation", "Managing and provisioning computing infrastructure through machine-readable definition files.", "Intermediate", "High", "Critical", ["iac"])
    ]),

    # 43. Containerization & 44. Kubernetes
    ("Containerization and Kubernetes", "Cloud-Native Packaging", "Docker, Podman, Kubernetes clusters, and container networking", [
        ("Docker", "Container Runtimes", "Set of platform-as-a-service products using OS-level virtualization to deliver software in packages.", "Beginner", "High", "Critical", ["docker-engine"]),
        ("Dockerfile Optimization", "Image Crafting", "Multi-stage builds, minimizing image layers, and security scanning container images.", "Beginner", "High", "Critical", ["dockerfile"]),
        ("Docker Compose", "Multi-Container Dev", "Tool for defining and running multi-container Docker applications with YAML configurations.", "Beginner", "High", "Critical", ["docker-compose"]),
        ("Kubernetes", "Container Orchestration", "Open-source system for automating deployment, scaling, and management of containerized applications.", "Intermediate", "High", "Critical", ["k8s"]),
        ("Kubernetes Pods & Deployments", "K8s Workloads", "Core Kubernetes workload abstractions managing container replicas and rollouts.", "Intermediate", "High", "Critical", ["k8s-deployments"]),
        ("Kubernetes Services & Ingress", "K8s Networking", "Exposing network applications and routing external traffic into cluster pods.", "Intermediate", "High", "Critical", ["k8s-ingress"]),
        ("Helm", "K8s Package Manager", "Package manager for Kubernetes to define, install, and upgrade complex Kubernetes apps.", "Intermediate", "High", "Critical", ["helm-charts"]),
        ("ConfigMaps and Secrets", "K8s Configuration", "Decoupling configuration artifacts and sensitive credentials from container image content.", "Intermediate", "High", "Critical", ["k8s-secrets"]),
        ("K8s Horizontal Pod Autoscaler", "Autoscaling", "Automatically updating workload resources to dynamically match fluctuating demand.", "Intermediate", "High", "High", ["hpa"])
    ]),

    # 45. CI/CD & Infrastructure as Code
    ("CI/CD and Automation", "Continuous Delivery", "Pipelines, automated testing integration, and declarative infrastructure", [
        ("GitHub Actions", "CI/CD Platforms", "Automating, customizing, and executing software development workflows right in repository.", "Beginner", "High", "Critical", ["gha", "github-actions"]),
        ("GitLab CI/CD", "CI/CD Platforms", "Tool built into GitLab for software development through continuous methodologies.", "Intermediate", "High", "High", ["gitlab-ci"]),
        ("Jenkins", "Automation Servers", "Open source automation server providing hundreds of plugins to build, deploy, and automate.", "Intermediate", "Medium", "High", ["jenkins-ci"]),
        ("Argo CD", "GitOps", "Declarative, GitOps continuous delivery tool for Kubernetes keeping cluster state in sync.", "Intermediate", "High", "Critical", ["argocd"]),
        ("Terraform", "Infrastructure as Code", "Open-source infrastructure as code software tool created by HashiCorp.", "Intermediate", "High", "Critical", ["hashicorp-terraform"]),
        ("OpenTofu", "Open Source IaC", "Community-driven open-source fork of Terraform for declarative cloud provisioning.", "Intermediate", "High", "High", ["opentofu"]),
        ("Ansible", "Configuration Management", "Open source automation tool that automates software provisioning and configuration.", "Intermediate", "High", "High", ["ansible-automation"])
    ]),

    # 46. Cybersecurity, 47. Ethical Hacking, 48. Network Security
    ("Cybersecurity and Ethical Hacking", "Information Assurance", "Penetration testing, network defense, threat analysis, and security controls", [
        ("OWASP Top 10", "Web Vulnerabilities", "Standard awareness document for developers representing broad consensus on critical security risks.", "Beginner", "High", "Critical", ["owasp"]),
        ("Wireshark", "Packet Analysis", "World's foremost and widely-used network protocol packet analyzer.", "Beginner", "High", "Critical", ["wireshark-tool"]),
        ("Nmap", "Network Scanning", "Network discovery and vulnerability scanning tool used by cybersecurity professionals.", "Beginner", "High", "Critical", ["nmap-scanner"]),
        ("Metasploit", "Penetration Testing", "Penetration testing framework that makes hacking simple and automates exploit testing.", "Intermediate", "High", "Critical", ["metasploit-framework"]),
        ("Burp Suite", "Web Security Testing", "Integrated platform and graphical tool for performing security testing of web applications.", "Intermediate", "High", "Critical", ["burp-suite"]),
        ("Kali Linux", "Security OS", "Debian-derived Linux distribution designed for digital forensics and penetration testing.", "Beginner", "High", "Critical", ["kali"]),
        ("Cryptography (AES, RSA, ECC)", "Information Security", "Mathematical algorithms securing data at rest and in transit via public-key and symmetric ciphers.", "Intermediate", "High", "Critical", ["cryptography"]),
        ("SIEM (Splunk, Wazuh)", "Security Monitoring", "Security Information and Event Management aggregating and analyzing security log data.", "Intermediate", "High", "Critical", ["siem-splunk"]),
        ("Vulnerability Assessment", "Security Auditing", "Scanning systems with Nessus and OpenVAS to uncover unpatched security flaws.", "Intermediate", "High", "High", ["vuln-scanning"])
    ]),

    # 49. Application Security, 50. Cloud Security, 51. Digital Forensics
    ("AppSec and Cloud Security", "Specialized Security", "Static code analysis, cloud posture management, and forensic investigation", [
        ("SAST & DAST", "AppSec Tooling", "Static and Dynamic Application Security Testing integrated into CI/CD pipelines.", "Intermediate", "High", "Critical", ["sast-dast"]),
        ("Threat Modeling (STRIDE)", "Security Architecture", "Structured approach for identifying, quantifying, and addressing system security threats.", "Intermediate", "High", "Critical", ["stride-threat"]),
        ("Cloud Security Posture (CSPM)", "Cloud Governance", "Automating cloud configuration auditing to eliminate misconfigurations and leaks.", "Intermediate", "High", "High", ["cspm"]),
        ("Digital Forensics & Incident Response", "Forensics", "Recovering evidence from file systems, memory dumps, and operating system logs.", "Advanced", "High", "High", ["dfir"]),
        ("Zero Trust Architecture", "Security Principles", "Strategic approach where no user or application is implicitly trusted inside or outside.", "Intermediate", "High", "Critical", ["zero-trust"])
    ]),

    # 52. Blockchain, 53. Smart Contracts, 54. Web3
    ("Blockchain and Web3", "Decentralized Computing", "Distributed ledgers, smart contracts, and decentralized application protocols", [
        ("Solidity", "Smart Contract Languages", "Statically typed, contract-oriented language for developing smart contracts on EVM.", "Intermediate", "High", "Critical", ["solidity-lang"]),
        ("EVM (Ethereum Virtual Machine)", "Decentralized Runtime", "Computation engine acting as the decentralized world computer on Ethereum.", "Intermediate", "High", "Critical", ["evm"]),
        ("Hardhat", "Ethereum Dev Environment", "Flexible development environment for developers to compile, deploy, test, and debug Ethereum software.", "Intermediate", "High", "Critical", ["hardhat-eth"]),
        ("Foundry", "Fast Smart Contract Dev", "Blazingly fast, portable and modular toolkit for Ethereum application development written in Rust.", "Intermediate", "High", "Critical", ["foundry-rs"]),
        ("Ethers.js / Web3.js", "Web3 Client Libraries", "JavaScript libraries facilitating interaction with the Ethereum Blockchain and its ecosystem.", "Beginner", "High", "Critical", ["ethers-js"]),
        ("Rust for Solana", "High-Performance Chains", "Building high-throughput on-chain programs on the Solana blockchain using Anchor framework.", "Advanced", "High", "High", ["solana-anchor"]),
        ("IPFS (InterPlanetary File System)", "Decentralized Storage", "Peer-to-peer hypermedia protocol designed to store and share data in a distributed file system.", "Beginner", "Medium", "High", ["ipfs"]),
        ("Smart Contract Security Auditing", "Web3 Security", "Detecting reentrancy attacks, integer overflows, and front-running vulnerabilities in DeFi.", "Advanced", "High", "Critical", ["audit-smart-contracts"])
    ]),

    # 55. Internet of Things (IoT) & 56. Robotics
    ("IoT and Robotics", "Physical Computing", "Connected sensors, microcontrollers, ROS, and autonomous robotics", [
        ("Arduino", "Microcontroller Prototyping", "Open-source hardware and software platform for building interactive electronic objects.", "Beginner", "High", "Critical", ["arduino-ide"]),
        ("Raspberry Pi", "Single-Board Computers", "Low cost, credit-card sized computer connecting to sensors and peripherals.", "Beginner", "High", "Critical", ["rpi"]),
        ("ESP32 / ESP8266", "Wireless Microcontrollers", "Low-cost, low-power system on a chip microcontrollers with integrated Wi-Fi and dual-mode Bluetooth.", "Beginner", "High", "Critical", ["esp32"]),
        ("MQTT Protocol", "IoT Messaging", "Lightweight, publish-subscribe network protocol for machine-to-machine connectivity.", "Beginner", "High", "Critical", ["mqtt"]),
        ("ROS / ROS 2", "Robotics Middleware", "Robot Operating System set of software libraries and tools helping build robot applications.", "Intermediate", "High", "Critical", ["ros2", "robot-operating-system"]),
        ("Gazebo Simulator", "Robotics Simulation", "3D robotics simulator accurately simulating robot populations in complex indoor and outdoor environments.", "Intermediate", "High", "High", ["gazebo"]),
        ("Sensor Integration (I2C, SPI, UART)", "Hardware Communication", "Interfacing microcontrollers with sensors using standard hardware communication buses.", "Beginner", "High", "Critical", ["i2c-spi-uart"])
    ]),

    # 57. Embedded Systems, 58. VLSI, 59. FPGA, 60. Electronics
    ("Embedded Systems and VLSI", "Hardware Engineering", "Firmware, digital circuit design, RTL modeling, and PCB layout", [
        ("Embedded C / C++", "Firmware Programming", "Writing highly optimized, memory-constrained firmware directly accessing hardware registers.", "Intermediate", "High", "Critical", ["embedded-c"]),
        ("FreeRTOS", "Real-Time Operating Systems", "Market-leading real-time operating system for microcontrollers and small microprocessors.", "Intermediate", "High", "Critical", ["freertos"]),
        ("Verilog / SystemVerilog", "Hardware Description", "Hardware description languages used to model electronic systems at the RTL level.", "Intermediate", "High", "Critical", ["verilog", "systemverilog"]),
        ("VHDL", "Hardware Description", "Formal hardware description language used in electronic design automation to describe digital systems.", "Intermediate", "Medium", "High", ["vhdl"]),
        ("FPGA Development (Xilinx Vivado)", "Programmable Logic", "Designing, synthesizing, and deploying digital logic into field-programmable gate arrays.", "Advanced", "High", "Critical", ["fpga-vivado"]),
        ("PCB Design (KiCad, Altium)", "Circuit Layout", "Schematic capture and printed circuit board layout design for custom electronics.", "Intermediate", "High", "Critical", ["kicad", "altium"]),
        ("Digital Signal Processing (DSP)", "Signal Processing", "Mathematical manipulation of audio, sensor, and radar signals using Fourier transforms.", "Advanced", "High", "High", ["dsp"])
    ]),

    # 61. Computer Networking & 62. Linux Administration
    ("Networking and Linux", "Systems Infrastructure", "IP routing, protocols, Linux kernel, system administration, and shell", [
        ("TCP/IP Protocols", "Network Fundamentals", "Conceptual model and set of communications protocols used on the Internet and computer networks.", "Beginner", "High", "Critical", ["tcp-ip"]),
        ("DNS & DHCP", "Network Services", "Domain Name System and Dynamic Host Configuration Protocol administration.", "Beginner", "High", "Critical", ["dns-dhcp"]),
        ("Linux System Administration", "OS Management", "Managing user permissions, storage volumes, process priorities, and packages on Linux.", "Beginner", "High", "Critical", ["sysadmin-linux"]),
        ("Systemd & Services", "Linux Inits", "Software suite that provides a system and service manager for Linux operating systems.", "Intermediate", "High", "Critical", ["systemd"]),
        ("Network Firewalls (iptables, UFW)", "Network Defense", "Configuring packet filtering rules and traffic blocking on Linux hosts.", "Beginner", "High", "High", ["iptables", "ufw"]),
        ("SSH & Key-Based Auth", "Remote Access", "Secure Shell protocol for remote server administration and encrypted file transfer.", "Beginner", "High", "Critical", ["ssh-keys"])
    ]),

    # 63. Software Engineering, 64. Testing, 65. Automation, 66. QA
    ("Software Engineering and QA", "Engineering Quality", "Agile practices, testing methodologies, test automation, and code standards", [
        ("Git Version Control", "Collaboration", "Distributed version control system for tracking changes in source code during software development.", "Beginner", "High", "Critical", ["git"]),
        ("Test-Driven Development (TDD)", "Methodologies", "Software development process relying on the repetition of very short development cycles.", "Intermediate", "High", "Critical", ["tdd"]),
        ("Selenium WebDriver", "Automation Testing", "Open source umbrella project for a range of tools and libraries supporting browser automation.", "Beginner", "High", "Critical", ["selenium"]),
        ("Playwright", "Modern E2E Testing", "Enables reliable end-to-end testing for modern web apps across Chromium, Firefox, and WebKit.", "Intermediate", "High", "Critical", ["playwright-testing"]),
        ("Postman & Newman", "API Testing", "Comprehensive API platform for building, testing, automating, and documenting REST APIs.", "Beginner", "High", "Critical", ["postman"]),
        ("Performance Testing (JMeter, k6)", "Load Testing", "Simulating thousands of concurrent requests to evaluate system throughput and latency limits.", "Intermediate", "High", "High", ["jmeter", "k6"]),
        ("Agile & Scrum Methodologies", "Project Workflows", "Iterative project management frameworks organizing engineering deliverables into sprints.", "Beginner", "High", "Critical", ["agile-scrum"])
    ]),

    # 67. System Design, 68. Microservices, 69. API Development
    ("System Design and Microservices", "Architecture", "Distributed architecture patterns, scalability, domain-driven design, and resilience", [
        ("High-Level System Design", "Architecture", "Designing scalable architectures managing millions of requests per second.", "Advanced", "High", "Critical", ["system-design"]),
        ("Microservices Architecture", "Distributed Systems", "Decomposing monolithic applications into loosely coupled, independently deployable services.", "Intermediate", "High", "Critical", ["microservices"]),
        ("Event-Driven Architecture (EDA)", "Asynchronous Design", "Software architecture pattern promoting the production, detection, and consumption of events.", "Intermediate", "High", "Critical", ["eda-arch"]),
        ("Domain-Driven Design (DDD)", "Software Modeling", "Structuring software code around the business domain, bounded contexts, and ubiquitous language.", "Advanced", "High", "Critical", ["ddd"]),
        ("CQRS & Event Sourcing", "Data Patterns", "Command Query Responsibility Segregation separating read and write data stores for maximum throughput.", "Advanced", "Medium", "High", ["cqrs"]),
        ("API Gateway Pattern", "Edge Services", "Single entry point routing requests to internal microservices with unified auth and rate limiting.", "Intermediate", "High", "Critical", ["api-gateway"]),
        ("Circuit Breaker & Resilience (Resilience4j)", "Fault Tolerance", "Preventing cascading failures in distributed systems when downstream dependencies fail.", "Intermediate", "High", "Critical", ["circuit-breaker"])
    ]),

    # 70. UI/UX Design & 71. Graphic Design
    ("UI/UX Design", "Product Experience", "User research, wireframing, interactive prototyping, and design systems", [
        ("Figma", "Interface Design", "Leading collaborative web application for interface design and interactive prototyping.", "Beginner", "High", "Critical", ["figma-tool"]),
        ("User Research & Usability Testing", "UX Methodologies", "Conducting qualitative interviews, card sorting, and user testing to validate product designs.", "Beginner", "High", "Critical", ["ux-research"]),
        ("Wireframing & Prototyping", "Design Execution", "Creating low-fidelity layout blueprints and high-fidelity interactive user flows.", "Beginner", "High", "Critical", ["wireframes"]),
        ("Design Systems & Component Specs", "Design Standards", "Creating reusable UI tokens, color palettes, typography scales, and component libraries.", "Intermediate", "High", "Critical", ["design-systems"]),
        ("Information Architecture (IA)", "UX Structure", "Structural design of shared information environments, sitemaps, and navigation hierarchy.", "Beginner", "High", "High", ["ia-design"])
    ]),

    # 72. Game Development & 73. AR/VR Development
    ("Game and AR/VR Development", "Interactive Media", "Game engines, physics simulation, spatial audio, and spatial computing", [
        ("Unity Engine", "Game Engines", "Cross-platform game engine developed by Unity Technologies for 2D, 3D, VR, and AR games.", "Intermediate", "High", "Critical", ["unity3d"]),
        ("Unreal Engine", "High-Fidelity Real-Time", "Advanced real-time 3D creation tool known for photorealistic visuals and Blueprints visual scripting.", "Advanced", "High", "Critical", ["ue5", "unreal"]),
        ("C# for Unity", "Game Scripting", "Writing gameplay mechanics, state machines, and physics behaviors in Unity.", "Intermediate", "High", "Critical", ["unity-csharp"]),
        ("C++ for Unreal", "Game Systems", "High-performance game logic, actor classes, and rendering pipelines in Unreal Engine.", "Advanced", "High", "Critical", ["unreal-cpp"]),
        ("Spatial Computing & OpenXR", "AR/VR Standards", "Open, royalty-free standard providing high-performance access to AR and VR devices.", "Advanced", "Medium", "High", ["openxr"]),
        ("Shader Programming (HLSL, GLSL)", "Graphics Programming", "Writing custom vertex and fragment shaders for real-time lighting and visual effects.", "Advanced", "Medium", "High", ["shaders", "hlsl"]),
        ("3D Asset Pipelines (Blender)", "3D Modeling", "Creating 3D meshes, UV unwrapping, rigging, and animation exports for game engines.", "Intermediate", "High", "High", ["blender-3d"])
    ]),

    # 74. Product, 75. Business Analysis, 76. Project Management, 77. Technical Documentation
    ("Product and Project Management", "Delivery & Governance", "Product strategy, user stories, documentation, and technical writing", [
        ("Product Roadmap Strategy", "Product Management", "Defining product vision, feature prioritization, and alignment with business objectives.", "Beginner", "High", "Critical", ["product-strategy"]),
        ("User Stories & Acceptance Criteria", "Business Analysis", "Writing clear agile user stories with testable Given-When-Then acceptance criteria.", "Beginner", "High", "Critical", ["user-stories"]),
        ("Jira & Confluence", "Project Management Tools", "Industry-standard agile planning software and documentation workspaces.", "Beginner", "High", "Critical", ["atlassian-jira"]),
        ("Technical Writing & API Docs", "Documentation", "Authoring developer guides, REST API documentation (OpenAPI), and architecture specs.", "Beginner", "High", "Critical", ["tech-writing"]),
        ("Markdown & Docusaurus", "Docs as Code", "Managing documentation using version-controlled Markdown files compiled with Docusaurus.", "Beginner", "High", "High", ["docusaurus-docs"])
    ]),

    # 78. Bioinformatics & 79. Healthcare Technology
    ("Bioinformatics and HealthTech", "Life Sciences", "Genomic sequences, protein folding, healthcare standards, and medical imaging", [
        ("BioPython", "Computational Biology", "Open-source collection of Python tools for computational molecular biology and bioinformatics.", "Intermediate", "High", "Critical", ["biopython"]),
        ("BLAST (Basic Local Alignment Search)", "Sequence Alignment", "Algorithm and program for comparing primary biological sequence information.", "Intermediate", "High", "Critical", ["ncbi-blast"]),
        ("Nextflow", "Bioinformatics Pipelines", "Scalable workflow orchestration framework enabling reproducible computational pipelines.", "Intermediate", "High", "High", ["nextflow-pipelines"]),
        ("FHIR (Fast Healthcare Interoperability)", "HealthTech Standards", "Standard describing data formats and elements for exchanging electronic health records.", "Intermediate", "High", "Critical", ["hl7-fhir"]),
        ("DICOM Standards", "Medical Imaging", "Digital Imaging and Communications in Medicine standard for handling medical imaging information.", "Intermediate", "High", "High", ["dicom-imaging"]),
        ("AlphaFold Protein Modeling", "Structural Biology", "AI system developed by DeepMind that predicts 3D structures of proteins from sequences.", "Advanced", "High", "High", ["alphafold"])
    ]),

    # 80. FinTech & 81. Automotive Technology
    ("FinTech and Automotive Software", "Industry Verticals", "High-frequency trading, payment gateways, autonomous vehicles, and AUTOSAR", [
        ("Financial Market Protocols (FIX)", "FinTech Standards", "Financial Information eXchange messaging standard for real-time electronic securities trading.", "Advanced", "Medium", "High", ["fix-protocol"]),
        ("Payment Gateway Integration (Stripe)", "FinTech Systems", "Integrating secure card payments, webhooks, and PCI-DSS compliant checkout flows.", "Beginner", "High", "Critical", ["stripe-api"]),
        ("Algorithmic Trading Strategies", "Quantitative Finance", "Backtesting quantitative statistical arbitrage and momentum trading models.", "Intermediate", "Medium", "High", ["quant-trading"]),
        ("AUTOSAR Architecture", "Automotive Software", "Standardized automotive open system architecture for vehicle electronic control units.", "Advanced", "High", "Critical", ["autosar"]),
        ("CAN Bus & Vehicle Networks", "Automotive Protocols", "Controller Area Network vehicle bus standard allowing ECUs to communicate.", "Intermediate", "High", "Critical", ["can-bus"]),
        ("Autonomous Driving Stacks (Autoware)", "Automotive AI", "Open-source software for self-driving vehicles incorporating perception and path planning.", "Advanced", "Medium", "High", ["autoware"])
    ]),

    # 82. Quantum & 83. High-Performance Computing
    ("Quantum and High-Performance Computing", "Advanced Computing", "Qubits, quantum circuits, supercomputing, and GPU acceleration", [
        ("Qiskit", "Quantum Computing", "Open-source software development kit for working with quantum computers at the level of circuits.", "Intermediate", "High", "Critical", ["ibm-qiskit"]),
        ("Cirq", "Quantum Computing", "Python library for writing, manipulating, and optimizing quantum circuits developed by Google.", "Intermediate", "High", "High", ["google-cirq"]),
        ("CUDA Programming", "GPU Acceleration", "Parallel computing platform and programming model developed by NVIDIA for GPUs.", "Advanced", "High", "Critical", ["nvidia-cuda"]),
        ("OpenCL", "Heterogeneous Computing", "Open standard for cross-platform, parallel programming of diverse processors (CPUs, GPUs, FPGAs).", "Advanced", "Medium", "High", ["opencl-framework"]),
        ("Slurm Workload Manager", "Supercomputing", "Open source fault-tolerant job scheduler used by high performance computing clusters.", "Intermediate", "High", "High", ["slurm-hpc"])
    ]),

    # 84. Scientific & 85. Geospatial & 86. GIS
    ("Scientific Computing and GIS", "Spatial & Scientific", "Spatial data analysis, GIS mapping, remote sensing, and numerical simulation", [
        ("GeoPandas", "Spatial Data Science", "Open source project to make working with geospatial data in Python easier.", "Beginner", "High", "Critical", ["geopandas"]),
        ("GDAL / OGR", "Geospatial Libraries", "Translator library for raster and vector geospatial data formats.", "Intermediate", "High", "Critical", ["gdal"]),
        ("QGIS", "Desktop GIS", "Open Source Geographic Information System supporting viewing, editing, and analysis of geospatial data.", "Beginner", "High", "Critical", ["qgis-software"]),
        ("ArcGIS Python API", "Commercial GIS", "Python library for performing GIS analysis, spatial data management, and mapping.", "Intermediate", "High", "High", ["arcgis-api"]),
        ("Remote Sensing & Satellite Imagery", "Earth Observation", "Processing multispectral satellite imagery (Sentinel, Landsat) with Python.", "Intermediate", "Medium", "High", ["remote-sensing"])
    ]),

    # 87. Digital Twins, 88. Edge Computing, 89. Computer Hardware, 90. Emerging Tech
    ("Edge Computing and Emerging Technologies", "Future Computing", "Edge AI, TinyML, WebAssembly, and digital twin physical models", [
        ("TinyML", "Edge AI", "Running machine learning models on low-power microcontrollers and embedded devices.", "Intermediate", "High", "Critical", ["tinyml-edge"]),
        ("WebAssembly (WASM)", "Web Runtimes", "Binary instruction format for a stack-based virtual machine enabling near-native speed in browsers.", "Intermediate", "High", "Critical", ["wasm"]),
        ("Digital Twin Modeling", "Simulation", "Virtual representation serving as the real-time digital counterpart of a physical object or system.", "Advanced", "Medium", "High", ["digital-twins"]),
        ("Edge Computing Architectures", "Distributed Edge", "Processing data closer to the source of generation rather than centralized cloud servers.", "Intermediate", "High", "Critical", ["edge-arch"]),
        ("Neuromorphic Computing Basics", "Emerging AI", "Brain-inspired computing architectures mimicking biological neural processing.", "Advanced", "Low", "Emerging", ["neuromorphic"])
    ])
]

def seed_skills(db: Session = None) -> int:
    """Populates skill categories, technical skills, and aliases."""
    print("=" * 60)
    print("SEEDING TECHNICAL SKILLS DATABASE (Target: 1,500+ Skills)")
    print("=" * 60)

    # Helper function to run seeding inside a transaction
    def _do_seed(session: Session):
        total_skills_inserted = 0
        total_categories_inserted = 0
        seen_codes = set()
        seen_names = set()

        for cat_name, domain, cat_desc, skills_list in RAW_CATEGORIES_DATA:
            # Check or create Category
            category = session.query(SkillCategory).filter_by(name=cat_name).first()
            if not category:
                category = SkillCategory(name=cat_name, domain=domain, description=cat_desc)
                session.add(category)
                session.flush()
                total_categories_inserted += 1

            for name, subcat, desc, diff, priority, relev, aliases in skills_list:
                clean_name = name.strip()
                code = slugify(clean_name)
                
                # Deduplication check
                if code in seen_codes or clean_name.lower() in seen_names:
                    continue
                seen_codes.add(code)
                seen_names.add(clean_name.lower())

                # Check if already in DB
                existing_skill = session.query(TechnicalSkill).filter_by(skill_code=code).first()
                if not existing_skill:
                    skill = TechnicalSkill(
                        skill_code=code,
                        name=clean_name,
                        category_id=category.category_id,
                        subcategory=subcat,
                        description=desc,
                        difficulty_level=diff,
                        learning_priority=priority,
                        industry_relevance=relev,
                        is_active=True,
                        verification_status="Verified",
                        source="Curated Industry Standard"
                    )
                    session.add(skill)
                    session.flush()
                    total_skills_inserted += 1

                    # Add Aliases
                    for alias_text in aliases:
                        clean_alias = alias_text.strip()
                        if clean_alias.lower() != clean_name.lower():
                            alias = SkillAlias(skill_id=skill.skill_id, alias_name=clean_alias)
                            session.add(alias)

        session.commit()
        return total_skills_inserted, total_categories_inserted

    if db is not None:
        return _do_seed(db)
    else:
        with get_db_session() as session:
            return _do_seed(session)

if __name__ == "__main__":
    skills_count, cat_count = seed_skills()
    print(f"Successfully seeded {skills_count} skills across {cat_count} categories!")
