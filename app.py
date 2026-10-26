# app.py
# Intelligent Career Path Planning System
# Technology: Python + Streamlit (Pure logic, no database, no complex frameworks)

import streamlit as st
from career_data import CAREER_DATABASE, AVAILABLE_SKILLS, AVAILABLE_INTERESTS
from logic import calculate_career_matches, analyze_skill_gap

# Page configuration
st.set_page_config(
    page_title="Intelligent Career Path Planning System",
    page_icon="🎓",
    layout="wide"
)

# Custom clean CSS styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1b3bbb;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .match-badge {
        background-color: #EFF6FF;
        color: #1b3bbb;
        font-weight: 800;
        font-size: 1.1rem;
        padding: 4px 12px;
        border-radius: 8px;
        border: 1px solid #BFDBFE;
    }
    .step-box {
        background-color: #F8FAFC;
        border-left: 4px solid #1b3bbb;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="main-title">🎓 Intelligent Career Path Planning System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">BE Artificial Intelligence & Data Science Mini-Project | Rule-Based Career Guidance</div>', unsafe_allow_html=True)

# Sidebar: Quick Sample Profile Loader for Viva Demonstration
st.sidebar.header("📋 Demo Controls")
st.sidebar.info("You can test manually or click the button below to load a sample student profile.")

sample_loaded = st.sidebar.button("Load Sample Student Profile (AI/ML)")

default_name = "Nadia Rachel" if sample_loaded else ""
default_degree = "BE Artificial Intelligence & Data Science" if sample_loaded else "BE Computer Engineering"
default_year = "3rd Year (Semester 6)" if sample_loaded else "3rd Year"
default_skills = ["Python", "SQL (Queries, Joins, GroupBy)", "NumPy & Pandas"] if sample_loaded else []
default_interests = ["Artificial Intelligence", "Machine Learning", "Generative AI"] if sample_loaded else []
default_goal = "Aspiring to become an AI Engineer building intelligent applications." if sample_loaded else ""

# ========================================================
# FEATURE 1: STUDENT DETAILS
# ========================================================
st.subheader("1️⃣ Student Profile & Academic Details")

with st.expander("Enter or Edit Your Student Profile", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Full Name", value=default_name, placeholder="e.g. John Doe")
        degree = st.text_input("Degree & Branch", value=default_degree, placeholder="e.g. BE AI & Data Science")
        academic_year = st.selectbox(
            "Current Academic Year",
            ["1st Year (Semester 1/2)", "2nd Year (Semester 3/4)", "3rd Year (Semester 5/6)", "4th Year (Semester 7/8)"],
            index=2 if sample_loaded else 0
        )

    with col2:
        selected_skills = st.multiselect(
            "Select Your Current Technical Skills",
            options=AVAILABLE_SKILLS,
            default=default_skills,
            help="Choose the skills you have already studied or practiced."
        )
        selected_interests = st.multiselect(
            "Select Your Areas of Interest",
            options=AVAILABLE_INTERESTS,
            default=default_interests,
            help="Choose fields that you enjoy learning about."
        )

    career_goal = st.text_input(
        "Career Aspiration / Goal (Optional)",
        value=default_goal,
        placeholder="e.g. Want to work as an AI Engineer or Data Scientist"
    )

st.divider()

# ========================================================
# FEATURE 2: CAREER RECOMMENDATIONS
# ========================================================
st.subheader("2️⃣ Career Recommendations & Compatibility Scoring")

# Run recommendation calculation
recommendations = calculate_career_matches(selected_skills, selected_interests)

st.write("Based on your skills and interests, here are the evaluated careers ranked by suitability:")

cols = st.columns(len(recommendations))
for idx, rec in enumerate(recommendations):
    with cols[idx]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:0.8rem; color:#64748B; font-weight:700;">RANK #{idx+1}</span>
                <span class="match-badge">{rec['match_score']}%</span>
            </div>
            <h4 style="margin:0 0 6px 0; color:#0F172A;">{rec['title']}</h4>
            <p style="font-size:0.8rem; color:#475569; min-height:50px;">{rec['description']}</p>
            <div style="font-size:0.75rem; color:#166534; margin-top:8px;">
                <strong>Matched Skills:</strong> {len(rec['matching_skills'])} of {rec['total_required']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ========================================================
# FEATURE 3: SKILL-GAP ANALYSIS
# ========================================================
st.subheader("3️⃣ Skill-Gap Analysis")

selected_career_key = st.selectbox(
    "Choose a Career to Analyze Your Skill Gap:",
    options=list(CAREER_DATABASE.keys()),
    index=0
)

target_career = CAREER_DATABASE[selected_career_key]
gap_info = analyze_skill_gap(selected_skills, selected_career_key)

col_summary, col_progress = st.columns([1, 2])
with col_summary:
    st.metric("Skill Match Ratio", f"{len(gap_info['acquired'])} / {gap_info['total_required']} Skills")
with col_progress:
    st.write(f"**Curriculum Readiness:** {gap_info['completion_percentage']}%")
    st.progress(gap_info['completion_percentage'] / 100.0)

gap_col1, gap_col2 = st.columns(2)

with gap_col1:
    st.markdown("#### ✅ Skills You Already Have")
    if gap_info["acquired"]:
        for s in gap_info["acquired"]:
            st.success(f"✓ **{s}** (Already declared in your profile)")
    else:
        st.info("You haven't declared any required skills for this role yet. Start with Step 1 in the roadmap below!")

with gap_col2:
    st.markdown("#### 🎯 Skills You Need to Learn")
    if gap_info["missing"]:
        for s in gap_info["missing"]:
            st.warning(f"+ **{s}** (Required for {selected_career_key})")
    else:
        st.balloons()
        st.success("Congratulations! You have reported all baseline skills for this role!")

st.divider()

# ========================================================
# FEATURE 4: CAREER ROADMAP
# ========================================================
st.subheader(f"4️⃣ Step-by-Step Learning Roadmap for {selected_career_key}")
st.write(f"Follow this structured 4-step preparation plan to build competency for the **{selected_career_key}** role:")

roadmap_steps = target_career["roadmap"]

for step_item in roadmap_steps:
    st.markdown(f"""
    <div class="step-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#1b3bbb; font-size:1rem;">{step_item['step']}</strong>
            <span style="font-size:0.75rem; background:#E2E8F0; padding:2px 8px; border-radius:4px; font-weight:600; color:#334155;">
                ⏱️ {step_item['duration']}
            </span>
        </div>
        <div style="font-size:0.85rem; color:#1E293B; margin-top:6px;">
            <strong>Topics:</strong> {step_item['topics']}
        </div>
        <div style="font-size:0.85rem; color:#0F766E; margin-top:4px;">
            <strong>🎯 Milestone:</strong> {step_item['milestone']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer Note for viva defense
st.markdown("---")
st.caption("🎓 **BE AI & Data Science Mini-Project:** Designed with deterministic rule-based logic and Python data structures. Simple, explainable, and viva-ready.")
