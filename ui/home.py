# ui/home.py
"""
Home / Executive Overview Dashboard View.
Displays macro platform statistics, quick search, featured career families,
and student profile summary.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import (
    TechnicalSkill, Career, AreaOfInterest, CareerPathway,
    Project, LearningResource, CareerCategory
)

def render_home():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%); padding: 2.2rem; border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.3); margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);">
        <h1 style="color: #ffffff; font-size: 2.4rem; font-weight: 800; margin-bottom: 0.5rem; letter-spacing: -0.5px;">
            🎓 Intelligent Career Path Planning System
        </h1>
        <p style="color: #c7d2fe; font-size: 1.15rem; font-weight: 400; max-width: 900px; line-height: 1.6; margin-bottom: 0;">
            A comprehensive, database-driven career intelligence platform bridging the gap between student education, technical proficiencies, and industry career opportunities across 50 specialized engineering domains.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        # 1. Platform Key Metrics
        total_skills = session.query(TechnicalSkill).count()
        total_careers = session.query(Career).count()
        total_interests = session.query(AreaOfInterest).count()
        total_pathways = session.query(CareerPathway).count()
        total_projects = session.query(Project).count()
        total_resources = session.query(LearningResource).count()

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        with m1:
            st.metric("Technical Skills", f"{total_skills:,}", "90 Domains")
        with m2:
            st.metric("Career Profiles", f"{total_careers:,}", "50 Families")
        with m3:
            st.metric("Interest Areas", f"{total_interests:,}", "27 Categories")
        with m4:
            st.metric("Career Pathways", f"{total_pathways:,}", "Vertical & Lateral")
        with m5:
            st.metric("Portfolio Projects", f"{total_projects:,}", "Real Capstones")
        with m6:
            st.metric("Learning Resources", f"{total_resources:,}", "Verified Links")

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 2. Quick Career Search & Student State Banner
        col_search, col_student = st.columns([1.6, 1])

        with col_search:
            st.subheader("🔍 Quick Career Search")
            all_career_titles = [c.title for c in session.query(Career.title).order_by(Career.title).all()]
            selected_quick_career = st.selectbox(
                "Search any of the 505 specialized career profiles:",
                all_career_titles,
                index=0,
                key="home_quick_search"
            )

            if selected_quick_career:
                c_obj = session.query(Career).filter_by(title=selected_quick_career).first()
                if c_obj:
                    st.markdown(f"""
                    <div style="background: rgba(30, 27, 75, 0.5); padding: 1rem; border-radius: 10px; border-left: 4px solid #8b5cf6; margin-top: 0.5rem;">
                        <div style="font-weight: 700; color: #f5f3ff; font-size: 1.1rem;">{c_obj.title}</div>
                        <div style="color: #a5b4fc; font-size: 0.9rem; margin-bottom: 0.4rem;">Family: {c_obj.category.name} | Subcategory: {c_obj.subcategory}</div>
                        <div style="color: #e2e8f0; font-size: 0.95rem;">{c_obj.description}</div>
                        <div style="margin-top: 0.6rem; color: #c4b5fd; font-size: 0.85rem;">
                            <strong>Entry Suitability:</strong> {c_obj.entry_level_suitability} | <strong>Difficulty:</strong> {c_obj.difficulty_level}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    btn_c1, btn_c2 = st.columns(2)
                    with btn_c1:
                        if st.button("📊 View Skill Gap Analysis", use_container_width=True):
                            st.session_state["target_career_id"] = c_obj.career_id
                            st.session_state["current_page"] = "Skill Gap Analyzer"
                            st.rerun()
                    with btn_c2:
                        if st.button("🗺️ Generate 8-Stage Roadmap", use_container_width=True):
                            st.session_state["target_career_id"] = c_obj.career_id
                            st.session_state["current_page"] = "Personalized 8-Stage Roadmap"
                            st.rerun()

        with col_student:
            st.subheader("👤 Your Profile Summary")
            student_skills = st.session_state.get("student_skills", {})
            student_interests = st.session_state.get("student_interests", [])
            academic_branch = st.session_state.get("academic_branch", "CSE")
            weekly_hours = st.session_state.get("weekly_hours", 15)

            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.6); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.25);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #94a3b8;">Academic Branch:</span>
                    <strong style="color: #f1f5f9;">{academic_branch}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #94a3b8;">Acquired Skills:</span>
                    <strong style="color: #10b981;">{len(student_skills)} skills</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #94a3b8;">Interest Areas:</span>
                    <strong style="color: #38bdf8;">{len(student_interests)} selected</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <span style="color: #94a3b8;">Weekly Study Budget:</span>
                    <strong style="color: #f59e0b;">{weekly_hours} hrs/week</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("✏️ Manage My Profile & Skills", use_container_width=True):
                st.session_state["current_page"] = "Student Profile & Skill Inventory"
                st.rerun()

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 2rem 0;'>", unsafe_allow_html=True)

        # 3. Featured Career Families Explorer
        st.subheader("🌐 Explore Top Career Families")
        categories = session.query(CareerCategory).order_by(CareerCategory.name).limit(8).all()
        f_cols = st.columns(4)

        for idx, cat in enumerate(categories):
            col = f_cols[idx % 4]
            careers_in_cat = len(cat.careers)
            with col:
                st.markdown(f"""
                <div style="background: rgba(30, 27, 75, 0.4); border: 1px solid rgba(139, 92, 246, 0.2); padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; min-height: 160px;">
                    <div style="font-weight: 700; color: #e0e7ff; font-size: 1.05rem; margin-bottom: 0.4rem;">{cat.name}</div>
                    <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.6rem; min-height: 48px;">{cat.description[:90]}...</div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="background: rgba(139, 92, 246, 0.2); color: #c4b5fd; font-size: 0.8rem; padding: 2px 8px; border-radius: 6px;">
                            {careers_in_cat} Careers
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Browse {cat.name[:14]}..", key=f"cat_btn_{cat.category_id}", use_container_width=True):
                    st.session_state["filter_category_id"] = cat.category_id
                    st.session_state["current_page"] = "Career Knowledge Base"
                    st.rerun()
