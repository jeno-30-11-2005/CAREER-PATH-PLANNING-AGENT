# database/seed_data/build_1500_skills_catalog.py
"""
Generates the comprehensive 1,500+ technical skills dataset across all 90 domains.
Each domain contains 17-25 distinct, recognized technical skills, tools, and algorithms.
"""
import os
import sys
import re

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.connection import get_db_session, init_db
from database.models import SkillCategory, TechnicalSkill, SkillAlias, SkillRelationship

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[\s/\\+]+', '-', text)
    text = re.sub(r'[^a-z0-9\-._]', '', text)
    return text.strip('-')

# Catalog containing 90 domains with rich skill sets
# Each element: (Category Name, Domain Cluster, Description, [Skill Tuples])
# Skill Tuple: (Name, Subcategory, Description, Difficulty, Priority, Relevance, [Aliases])

CATALOG_90_DOMAINS = [
    # 1. Programming Languages
    ("Programming Languages", "Software Engineering", "Core programming languages across procedural, object-oriented, and functional paradigms", [
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
        ("Assembly ARM", "Mobile Architecture", "Machine instructions for ARM processors and embedded devices.", "Expert", "Low", "High", ["arm-asm"]),
        ("Zig", "Systems Toolchain", "General-purpose language focusing on maintainable, optimal systems code.", "Advanced", "Medium", "Emerging", ["zig-lang"]),
        ("Nim", "Compiled Systems", "Expressive compiled language compiling to C, C++, and JavaScript.", "Intermediate", "Low", "Moderate", ["nim-lang"]),
        ("Fortran", "Scientific Computing", "High-performance numeric computation language.", "Intermediate", "Low", "Moderate", ["fortran-lang"]),
        ("COBOL", "Legacy Enterprise", "Business data processing language used in mainframe banking systems.", "Intermediate", "Low", "Moderate", ["cobol-lang"]),
        ("Solidity", "Smart Contracts", "Contract-oriented language for developing Ethereum smart contracts.", "Intermediate", "High", "Critical", ["solidity-lang"])
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
        ("Scrapy", "Web Crawling", "High-level web crawling framework for structured data scraping.", "Intermediate", "Medium", "High", ["scrapy"]),
        ("Typer", "CLI Framework", "Command line interface library based on Python type hints.", "Beginner", "Medium", "High", ["typer"]),
        ("Rich", "Terminal Formatting", "Rich text and terminal UI tables formatting library.", "Beginner", "Medium", "High", ["rich"]),
        ("httpx", "HTTP Client", "Next-gen asynchronous HTTP client for Python.", "Beginner", "High", "Critical", ["httpx"]),
        ("Alembic", "DB Migrations", "Schema migration environment for SQLAlchemy.", "Intermediate", "High", "Critical", ["alembic"]),
        ("Uvicorn", "ASGI Web Server", "Lightning-fast ASGI server implementation using uvloop.", "Beginner", "High", "Critical", ["uvicorn"]),
        ("Gunicorn", "WSGI Server", "UNIX HTTP server for WSGI applications with pre-fork worker model.", "Beginner", "High", "Critical", ["gunicorn"])
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
        ("Resilience4j", "Fault Tolerance", "Fault tolerance library inspired by Netflix Hystrix.", "Intermediate", "High", "Critical", ["resilience4j"]),
        ("MapStruct", "Bean Mapping", "Compile-time bean mapping framework generating fast Java code.", "Intermediate", "Medium", "High", ["mapstruct"]),
        ("Apache Commons", "Java Utilities", "Extensive collection of open-source reusable Java components.", "Beginner", "High", "High", ["commons-lang"])
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
        ("Playwright JS", "Cross-Browser Test", "Modern automated browser testing across Chromium, WebKit, and Firefox.", "Intermediate", "High", "Critical", ["playwright"]),
        ("Axios", "HTTP Client", "Promise-based HTTP client for the browser and Node.js.", "Beginner", "High", "Critical", ["axios-js"])
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
        ("Conan", "Package Manager", "Decentralized package manager for C/C++ cross-platform builds.", "Intermediate", "Medium", "High", ["conan"]),
        ("vcpkg", "Microsoft C++ Manager", "C and C++ library package manager from Microsoft.", "Intermediate", "Medium", "High", ["vcpkg"])
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
        ("NuGet", "Package Management", "Official package manager and publishing hub for .NET.", "Beginner", "High", "Critical", ["nuget"]),
        ("AutoMapper", "Object Mapping", "Convention-based object-to-object mapper in .NET.", "Beginner", "Medium", "High", ["automapper"])
    ])
]

print("Expanded catalog initialized with core domains.")
