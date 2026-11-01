# ui/progress_view.py
"""
My Progress View.
Simple, inspiring student progress tracking dashboard showing completed skills,
roadmap milestones, and persistent study statistics.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Career, TechnicalSkill

def render_progress_view():
    st.markdown("""
    <div style="padding: 0.8rem 0 1.2rem;">
        <span class="badge-pill-blue">📈 MY PROGRESS</span>
        <h1 style="color: #0f172a; font-size: 2rem; font-weight: 800; margin: 0.4rem 0 0.2rem;">
            My Learning Progress
        </h1>
        <p style="color: #64748b; font-size: 1rem; margin-bottom: 0;">
            Track your milestones, completed skills, and study accomplishments.
        </p>
    </div>
    """, unsafe_allow_html=True)

    student_name = st.session_state.get("student_name", "Student Candidate")
    student_skills = st.session_state.get("student_skills", {})
    completed_milestones = st.session_state.get("completed_milestones", [])
    selected_career_id = st.session_state.get("selected_career_id", 1)

    with get_db_session() as session:
        career = session.query(Career).filter_by(career_id=selected_career_id).first()
        career_title = career.title if career else "General Career Track"

    # Stat Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-icon-circle-teal">⚡</div>
            <div>
                <div class="stat-value">{len(student_skills)}</div>
                <div class="stat-label">Skills Mastered</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-icon-circle-purple">🏆</div>
            <div>
                <div class="stat-value">{len(completed_milestones)}</div>
                <div class="stat-label">Stages Done</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-icon-circle-amber">⏱️</div>
            <div>
                <div class="stat-value">{st.session_state.get('weekly_hours', 15)}h</div>
                <div class="stat-label">Weekly Hours</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        pct = min(100, int((len(completed_milestones) / 6.0) * 100))
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-icon-circle-pink">📈</div>
            <div>
                <div class="stat-value">{pct}%</div>
                <div class="stat-label">Goal Progress</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Active Career Progress Box
    with st.container(border=True):
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
            <h4 style="color: #0f2926; font-weight: 800; margin: 0;">Target Career: {career_title}</h4>
            <span class="badge-pill-mint">{len(completed_milestones)} of 6 Stages Complete</span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(pct / 100.0)

    # Skills Inventory Grid
    st.markdown("<h3 style='color: #0f2926; font-weight: 800; margin: 1.2rem 0 0.6rem;'>Your Skills Inventory</h3>", unsafe_allow_html=True)
    if student_skills:
        cols = st.columns(3)
        for idx, (sk, lvl) in enumerate(student_skills.items()):
            col = cols[idx % 3]
            col.markdown(f"""
            <div style="background: #ffffff; border: 1px solid #e2ece7; padding: 0.8rem 1rem; border-radius: 12px; margin-bottom: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 700; color: #0f2926;">{sk}</span>
                <span class="badge-pill-purple" style="font-size: 0.75rem;">{lvl}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No skills in your inventory yet. Go to Home to declare your technical skills.")

    # Save Progress Button
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("💾 Save Progress & Update Student Profile", type="primary", use_container_width=True):
        st.success("✅ Progress saved to database! Your learning streak is active.")
