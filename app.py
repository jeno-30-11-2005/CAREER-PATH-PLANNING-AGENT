# app.py
"""
Intelligent Career Path Planning System - Career Guide Platform.
Redesigned with a Simple, Friendly, Beginner-Ready Interface
for school, plus two, and college students.
"""
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Career Guide",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Simple, Friendly, Clean Theme (White Background, Approachable Typography)
st.markdown("""
<style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Body & Background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Light, Clean Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 1px 0 10px rgba(0, 0, 0, 0.02) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1e293b !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        letter-spacing: -0.2px !important;
    }

    /* Universal Label & Text Contrast */
    label, 
    .stTextInput label, 
    .stSelectbox label, 
    .stMultiSelect label, 
    .stSlider label, 
    .stFileUploader label, 
    .stTextArea label,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] label {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    div[data-testid="stMarkdownContainer"] p {
        color: #334155 !important;
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
    }

    /* Fix Streamlit Sliders */
    div[data-testid="stSlider"] * {
        color: #0f172a !important;
    }
    div[data-testid="stSlider"] div[data-testid="stTickBarMin"],
    div[data-testid="stSlider"] div[data-testid="stTickBarMax"] {
        color: #64748b !important;
    }

    /* Fix Streamlit Tabs */
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: 700 !important;
        background: transparent !important;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #2563eb !important;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"] div,
    div[data-testid="stTabs"] button[data-baseweb="tab"] p {
        color: inherit !important;
    }

    /* Material Symbols font protection */
    [data-testid="stIconMaterial"], 
    .material-symbols-rounded,
    .material-symbols-outlined,
    span[data-testid="stExpanderToggleIcon"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        display: inline-block !important;
        vertical-align: middle !important;
        line-height: 1 !important;
    }

    /* Fix Streamlit Expander */
    div[data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        margin-bottom: 0.8rem !important;
        overflow: hidden !important;
    }
    div[data-testid="stExpander"] details summary {
        color: #0f172a !important;
        font-weight: 700 !important;
        padding: 0.8rem 1rem !important;
        cursor: pointer !important;
    }
    div[data-testid="stExpander"] details summary p {
        color: #0f172a !important;
        font-weight: 700 !important;
        margin: 0 !important;
        margin-left: 0.5rem !important;
    }

    /* Container Border Card Styling */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 1.25rem 1.4rem !important;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 1.25rem !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #cbd5e1 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
    }

    /* Fix Streamlit File Uploader */
    div[data-testid="stFileUploader"] {
        background: transparent !important;
    }
    div[data-testid="stFileUploader"] label,
    div[data-testid="stFileUploader"] label p,
    div[data-testid="stFileUploader"] label span {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    div[data-testid="stFileUploader"] section {
        background: #f8fafc !important;
        border: 2px dashed #93c5fd !important;
        border-radius: 14px !important;
        padding: 1.4rem !important;
    }
    div[data-testid="stFileUploader"] section * {
        color: #1e293b !important;
    }
    div[data-testid="stFileUploader"] section button {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.4rem 1rem !important;
    }
    div[data-testid="stFileUploader"] section button * {
        color: #ffffff !important;
    }
    div[data-testid="stFileUploader"] section small {
        color: #64748b !important;
    }

    /* Fix Streamlit Inputs & Selectboxes */
    input, textarea {
        color: #0f172a !important;
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
    }
    div[data-baseweb="select"] * {
        color: #0f172a !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    ul[data-baseweb="menu"],
    li[data-baseweb="menu-item"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    li[data-baseweb="menu-item"]:hover {
        background-color: #eff6ff !important;
        color: #1d4ed8 !important;
    }

    /* Multiselect Tags */
    span[data-baseweb="tag"] {
        background-color: #eff6ff !important;
        border: 1px solid #bfdbfe !important;
        border-radius: 8px !important;
    }
    span[data-baseweb="tag"] span {
        color: #1d4ed8 !important;
        font-weight: 700 !important;
    }

    /* Friendly Simple Banner */
    .banner-friendly {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 2rem 2.2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
    }

    /* Badges & Pills */
    .badge-pill-blue {
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
    }
    .badge-pill-green {
        background: #f0fdf4;
        color: #15803d;
        border: 1px solid #bbf7d0;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
    }
    .badge-pill-amber {
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
    }
    .badge-pill-purple {
        background: #f5f3ff;
        color: #6d28d9;
        border: 1px solid #ddd6fe;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
    }

    /* Skill tags */
    .skill-pill-matched {
        background: #f0fdf4;
        color: #15803d;
        border: 1px solid #bbf7d0;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 8px;
        display: inline-block;
        margin: 2px 4px 2px 0;
    }
    .skill-pill-missing {
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 8px;
        display: inline-block;
        margin: 2px 4px 2px 0;
    }

    /* Primary & Secondary Buttons */
    button[kind="primary"] {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.4rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"] * {
        color: #ffffff !important;
    }
    button[kind="primary"]:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    button[kind="secondary"] {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    button[kind="secondary"] * {
        color: #1e293b !important;
    }
    button[kind="secondary"]:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #2563eb 0%, #38bdf8 100%) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if "student_name" not in st.session_state:
    st.session_state["student_name"] = "Alex Morgan"

if "education_level" not in st.session_state:
    st.session_state["education_level"] = "Undergraduate (B.Tech / B.E.)"

if "academic_branch" not in st.session_state:
    st.session_state["academic_branch"] = "Computer Science & Engineering (CSE)"

if "current_semester" not in st.session_state:
    st.session_state["current_semester"] = "3rd Year (Semester 5-6)"

if "student_skills" not in st.session_state:
    st.session_state["student_skills"] = {
        "Python": "Advanced",
        "FastAPI": "Intermediate",
        "SQL (PostgreSQL)": "Intermediate",
        "Docker Containerization": "Beginner"
    }

if "student_interests" not in st.session_state:
    st.session_state["student_interests"] = [
        "Artificial Intelligence",
        "Machine Learning & Data Science",
        "Full Stack Web Development"
    ]

if "weekly_hours" not in st.session_state:
    st.session_state["weekly_hours"] = 15

if "completed_milestones" not in st.session_state:
    st.session_state["completed_milestones"] = []

if "current_view" not in st.session_state:
    st.session_state["current_view"] = "Home"

# 4. Import Views
from ui.single_page_home import render_single_page_home
from ui.career_plan_view import render_career_plan_view
from ui.progress_view import render_progress_view
from ui.tools_view import render_tools_view

# 5. Sidebar Navigation (Simple, Friendly & Clean)
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.2rem;">
        <span class="badge-pill-blue">🎓 CAREER GUIDE</span>
        <h2 style="color: #0f172a; font-size: 1.35rem; font-weight: 800; margin: 0.4rem 0 0.1rem;">Career Guide</h2>
        <div style="color: #64748b; font-size: 0.85rem; line-height: 1.4;">Find What You Like.<br>Discover What You Can Become.</div>
    </div>
    """, unsafe_allow_html=True)

    nav_options = [
        "🏠 Home",
        "📋 My Plan",
        "📈 My Progress",
        "🧰 More Tools"
    ]

    curr_idx = 0
    if st.session_state["current_view"] == "My Plan" or st.session_state["current_view"] == "My Career Plan":
        curr_idx = 1
    elif st.session_state["current_view"] == "My Progress":
        curr_idx = 2
    elif st.session_state["current_view"] == "More Tools":
        curr_idx = 3

    selected_nav = st.radio(
        "Menu:",
        nav_options,
        index=curr_idx,
        label_visibility="collapsed"
    )

    clean_view = selected_nav.split(" ", 1)[1]
    if clean_view != st.session_state["current_view"]:
        st.session_state["current_view"] = clean_view
        st.rerun()

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.caption("A simple guide for school and college students to explore their future careers.")

# 6. Render Active View
if st.session_state["current_view"] == "Home":
    render_single_page_home()
elif st.session_state["current_view"] in ["My Plan", "My Career Plan"]:
    render_career_plan_view()
elif st.session_state["current_view"] == "My Progress":
    render_progress_view()
elif st.session_state["current_view"] == "More Tools":
    render_tools_view()
