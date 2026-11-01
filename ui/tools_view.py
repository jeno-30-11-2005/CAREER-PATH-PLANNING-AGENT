# ui/tools_view.py
"""
More Tools View.
Provides access to optional advanced features:
- AI Resume Analyzer (PyMuPDF & python-docx extraction)
- Career Comparison Tool (Side-by-side comparison of 2-3 careers)
- Admin Management Portal (System statistics, bulk import, audit logs)
"""
import streamlit as st
from ui.resume_analyzer import render_resume_analyzer
from ui.comparison import render_comparison
from ui.admin_dashboard import render_admin_dashboard

def render_tools_view():
    st.markdown("""
    <div style="padding: 0.8rem 0 1.2rem;">
        <span class="badge-pill-blue">🧰 MORE TOOLS</span>
        <h1 style="color: #0f172a; font-size: 2rem; font-weight: 800; margin: 0.4rem 0 0.2rem;">
            Advanced Career Tools
        </h1>
        <p style="color: #64748b; font-size: 1rem; margin-bottom: 0;">
            Optional tools to analyze your resume, compare careers side-by-side, or manage the database.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tool_choice = st.radio(
        "Choose Tool:",
        ["📄 AI Resume Analyzer", "⚖️ Career Comparison Tool", "⚙️ Admin Portal"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    if tool_choice == "📄 AI Resume Analyzer":
        render_resume_analyzer()
    elif tool_choice == "⚖️ Career Comparison Tool":
        render_comparison()
    elif tool_choice == "⚙️ Admin Portal":
        render_admin_dashboard()
