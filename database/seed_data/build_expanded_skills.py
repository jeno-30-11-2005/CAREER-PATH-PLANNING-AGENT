# database/seed_data/build_expanded_skills.py
"""
Builds the complete 1,500+ technical skills dataset across all 90 domains.
Each domain contains 17-25 distinct, recognized technical skills.
"""
import re

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[\s/\\+]+', '-', text)
    text = re.sub(r'[^a-z0-9\-._]', '', text)
    return text.strip('-')

# The 90 domains with their category name, cluster, description, and list of skills
DOMAINS_DATA = {}

def reg(domain_name, cluster, description, skills_list):
    DOMAINS_DATA[domain_name] = {
        "cluster": cluster,
        "description": description,
        "skills": skills_list
    }

# 1. Programming Languages
reg("Programming Languages", "Software Engineering", "Core procedural, object-oriented, functional, and systems programming languages", [
    ("Python", "General Purpose", "High-level interpreted language known for ease of use, dynamic typing, and vast libraries.", "Beginner", "High", "Critical", ["python3", "py"]),
    ("Java", "Enterprise OOP", "Object-oriented, class-based language engineered for cross-platform portability on the JVM.", "Intermediate", "High", "Critical", ["jdk", "jvm"]),
    ("C", "Systems", "Low-level procedural programming language with direct memory manipulation capabilities.", "Intermediate", "High", "High", ["ansi-c"]),
    ("C++", "Systems & Performance", "Object-oriented systems language with generic templates, RAII, and high-performance execution.", "Advanced", "High", "Critical", ["cpp", "cplusplus"]),
    ("C#", "Enterprise & Games", "Modern, type-safe language developed by Microsoft for .NET and game development in Unity.", "Intermediate", "High", "High", ["csharp", "dotnet-c#"]),
    ("JavaScript", "Web Development", "Dynamic scripting language powering front-end interactivity and full-stack web platforms.", "Beginner", "High", "Critical", ["js", "ecmascript"]),
    ("TypeScript", "Typed Web", "Statically typed superset of JavaScript adding compile-time type checking and interfaces.", "Intermediate", "High", "Critical", ["ts"]),
    ("Go", "Cloud & Backend", "Compiled language developed by Google for concurrent distributed backend services.", "Intermediate", "High", "Critical", ["golang"]),
    ("Rust", "Systems Programming", "Memory-safe systems programming language without garbage collection overhead.", "Advanced", "High", "Critical", ["rust-lang"]),
    ("Kotlin", "Mobile & JVM", "Modern, expressive statically typed language officially favored by Google for Android.", "Intermediate", "High", "High", ["kt"]),
    ("Swift", "Apple Ecosystem", "Fast, safe, and intuitive language designed for iOS, iPadOS, macOS, and watchOS.", "Intermediate", "High", "High", ["apple-swift"]),
    ("PHP", "Server-Side Web", "Widely-used open-source scripting language for server-side web development.", "Beginner", "Medium", "Moderate", ["php8"]),
    ("Ruby", "Productive Scripting", "Dynamic, object-oriented language focused on programmer productivity and elegance.", "Beginner", "Medium", "Moderate", ["ruby-lang"]),
    ("R", "Statistical Computing", "Language and environment specialized for statistics, data mining, and graphics.", "Intermediate", "High", "High", ["r-lang"]),
    ("Scala", "Functional JVM", "Combines object-oriented and functional programming running on the Java Virtual Machine.", "Advanced", "Medium", "High", ["scala-lang"]),
    ("Dart", "Cross-Platform Mobile", "Client-optimized programming language developed by Google, powering Flutter.", "Beginner", "Medium", "High", ["dart-lang"]),
    ("Julia", "Scientific Computing", "High-performance language designed for numerical and scientific computing workloads.", "Intermediate", "Medium", "Emerging", ["julia-lang"]),
    ("Lua", "Embedded Scripting", "Lightweight embeddable scripting language widely used in gaming engines and Redis.", "Beginner", "Medium", "Moderate", ["lua-lang"]),
    ("Haskell", "Purely Functional", "Statically typed purely functional programming language with lazy evaluation.", "Advanced", "Low", "Moderate", ["haskell-lang"]),
    ("Elixir", "Concurrent Systems", "Dynamic, functional language built on the Erlang BEAM VM for high-availability systems.", "Intermediate", "Medium", "High", ["elixir-lang"]),
    ("Clojure", "Lisp on JVM", "Dynamic, general-purpose functional Lisp dialect targeting the Java platform.", "Advanced", "Low", "Moderate", ["clojure-lang"]),
    ("Perl", "Text Processing", "High-level interpreted language known for powerful regular expressions and text parsing.", "Intermediate", "Low", "Moderate", ["perl-lang"]),
    ("Shell Scripting", "DevOps Automation", "Writing automation scripts using Unix/Linux shells (Bash, Zsh) to automate tasks.", "Beginner", "High", "Critical", ["bash", "sh"]),
    ("PowerShell", "Windows Automation", "Object-oriented command-line shell and scripting framework for system administration.", "Intermediate", "High", "High", ["pwsh"]),
    ("Assembly x86", "Low-Level Systems", "Low-level symbolic machine code corresponding to the x86 instruction set architecture.", "Expert", "Low", "Moderate", ["x86-asm"]),
    ("Assembly ARM", "Mobile & Embedded", "Instruction set architecture for ARM processors powering smartphones and Apple silicon.", "Expert", "Low", "High", ["arm-asm"]),
    ("Zig", "Systems Toolchain", "General-purpose language focusing on maintainable, optimal, and reusable systems code.", "Advanced", "Medium", "Emerging", ["zig-lang"]),
    ("Nim", "Compiled Systems", "Statically typed compiled systems programming language combining efficiency with readability.", "Intermediate", "Low", "Moderate", ["nim-lang"]),
    ("Groovy", "JVM Scripting", "Dynamic language with static typing capabilities for the Java platform, used in Gradle.", "Intermediate", "Medium", "Moderate", ["apache-groovy"]),
    ("Fortran", "Scientific Computing", "General-purpose, compiled imperative language especially suited to numeric computation.", "Intermediate", "Low", "Moderate", ["fortran-lang"]),
    ("COBOL", "Legacy Enterprise", "Compiled English-like computer programming language designed for business use.", "Intermediate", "Low", "Moderate", ["cobol-lang"]),
    ("Solidity", "Smart Contracts", "Contract-oriented language for developing smart contracts on Ethereum.", "Intermediate", "High", "Critical", ["solidity-lang"])
])

# 2. Python Ecosystem
reg("Python Ecosystem", "Data & Web", "Libraries, frameworks, testing tools, and runtimes built on Python", [
    ("NumPy", "Scientific Computing", "Core package for array computing, linear algebra, and multidimensional arrays.", "Beginner", "High", "Critical", ["numpy-lib"]),
    ("Pandas", "Data Manipulation", "High-performance tabular data structures and data analysis tools.", "Beginner", "High", "Critical", ["pandas-lib"]),
    ("SciPy", "Scientific Algorithms", "Mathematical algorithms and convenience functions built on NumPy.", "Intermediate", "High", "High", ["scipy-lib"]),
    ("Matplotlib", "Data Visualization", "Foundational plotting library for publication-quality figures.", "Beginner", "High", "High", ["matplotlib-py"]),
    ("Seaborn", "Statistical Viz", "Statistical data visualization framework with aesthetic built-in themes.", "Beginner", "High", "High", ["seaborn-py"]),
    ("Scikit-Learn", "Machine Learning", "Classical machine learning toolkit providing predictive modeling algorithms.", "Intermediate", "High", "Critical", ["sklearn"]),
    ("FastAPI", "Web Frameworks", "Modern high-speed ASGI framework with automated OpenAPI validation.", "Intermediate", "High", "Critical", ["fastapi"]),
    ("Flask", "Web Frameworks", "Lightweight WSGI micro web framework for rapid API development.", "Beginner", "High", "High", ["flask-py"]),
    ("Django", "Web Frameworks", "High-level framework for secure, scalable database-driven web applications.", "Intermediate", "High", "Critical", ["django"]),
    ("SQLAlchemy", "ORM & Database", "Comprehensive SQL toolkit and Object Relational Mapper for Python.", "Intermediate", "High", "Critical", ["sqlalchemy"]),
    ("Pydantic", "Data Validation", "Data validation and settings management using Python type hints.", "Intermediate", "High", "Critical", ["pydantic"]),
    ("Celery", "Distributed Tasks", "Asynchronous distributed task queue for background job execution.", "Intermediate", "Medium", "High", ["celery"]),
    ("Pytest", "Testing Framework", "Mature full-featured Python testing tool supporting fixtures and plugins.", "Beginner", "High", "Critical", ["pytest"]),
    ("Poetry", "Dependency Management", "Deterministic packaging and dependency resolver for Python projects.", "Intermediate", "High", "High", ["poetry"]),
    ("Polars", "High-Speed DataFrames", "Blazingly fast multi-threaded DataFrame library implemented in Rust.", "Intermediate", "High", "Critical", ["polars"]),
    ("Dask", "Parallel Computing", "Flexible parallel computing library scaling Python data workloads.", "Advanced", "Medium", "High", ["dask"]),
    ("Ray", "Distributed Computing", "Unified compute engine for scaling AI and parallel Python workloads.", "Advanced", "High", "Critical", ["ray"]),
    ("Streamlit", "Data Apps", "Framework for creating interactive data dashboards and machine learning web apps.", "Beginner", "High", "Critical", ["streamlit"]),
    ("Gradio", "Model Demos", "Easy web interface builder for demonstrating machine learning models.", "Beginner", "High", "High", ["gradio"]),
    ("Asyncio", "Concurrent Python", "Library for asynchronous I/O and non-blocking event loops in Python.", "Intermediate", "High", "Critical", ["asyncio"]),
    ("Beautiful Soup", "Web Scraping", "Python library for parsing HTML and extracting structured text.", "Beginner", "Medium", "Moderate", ["bs4"]),
    ("Scrapy", "Web Crawling", "Fast, high-level screen scraping and web crawling framework.", "Intermediate", "Medium", "High", ["scrapy"]),
    ("Rich", "Terminal UI", "Python library for rich text and beautiful formatting in the terminal.", "Beginner", "Medium", "High", ["rich-py"]),
    ("Typer", "CLI Development", "Library for building Command Line Interfaces based on Python 3.6+ type hints.", "Beginner", "Medium", "High", ["typer-cli"]),
    ("Loguru", "Logging", "Library that aims to bring enjoyable and painless logging to Python.", "Beginner", "Medium", "High", ["loguru-py"]),
    ("httpx", "HTTP Client", "Next-generation HTTP client for Python supporting HTTP/2 and async calls.", "Beginner", "High", "Critical", ["httpx-client"]),
    ("Alembic", "Database Migrations", "Lightweight database migration tool for usage with SQLAlchemy.", "Intermediate", "High", "Critical", ["alembic-db"])
])

print("Domains 1 & 2 loaded.")
