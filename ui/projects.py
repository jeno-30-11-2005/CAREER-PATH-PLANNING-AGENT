# ui/projects.py
"""
Practical Portfolio Projects View.
Browse 500+ practical portfolio capstone ideas with detailed problem statements,
step-by-step implementation plans, deliverables, and mapped technical skills.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Project, Career
from services.project_service import ProjectService

def render_projects():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">📁 Practical Portfolio Projects</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Explore 500+ production-grade portfolio project specifications designed to prove real-world engineering readiness to hiring managers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        f_c1, f_c2, f_c3 = st.columns([2, 1.2, 1])

        with f_c1:
            search_query = st.text_input("🔍 Search projects by title, stack, or problem:", placeholder="e.g. Microservice, RAG, Kubernetes, Computer Vision...")

        with f_c2:
            all_cats = [row[0] for row in session.query(Project.category).distinct().order_by(Project.category).all() if row[0]]
            selected_cat = st.selectbox("Project Category:", ["All Categories"] + all_cats)

        with f_c3:
            selected_diff = st.selectbox("Difficulty:", ["All", "Beginner", "Intermediate", "Advanced"])

        cat_arg = None if selected_cat == "All Categories" else selected_cat
        diff_arg = None if selected_diff == "All" else selected_diff

        projects = ProjectService.get_all_projects(
            session=session,
            category=cat_arg,
            difficulty=diff_arg,
            search_query=search_query,
            limit=40
        )

        st.markdown(f"<div style='color: #a5b4fc; margin-bottom: 1rem;'>Showing <strong>{len(projects)}</strong> projects:</div>", unsafe_allow_html=True)

        for p in projects:
            with st.expander(f"📦 {p['title']} ({p['category']} | {p['difficulty']})", expanded=False):
                col_left, col_right = st.columns([2.2, 1])

                with col_left:
                    st.markdown(f"**Target Role:** `{p['career_title']}` | **Type:** `{p['project_type']}` | **Est. Time:** `{p['estimated_hours']} hrs`")
                    st.markdown(f"**Problem Statement:** {p['problem_statement']}")
                    st.markdown(f"**Objective:** {p['objective']}")
                    
                    st.markdown("##### 🛠️ Suggested Technologies:")
                    st.markdown(f"`{p['suggested_technologies']}`")

                    st.markdown("##### 📋 Implementation Steps:")
                    st.text(p['implementation_steps'])

                    st.markdown("##### 🎯 Expected Deliverables:")
                    st.text(p['expected_deliverables'])

                    st.markdown("##### 💡 Learning Outcomes:")
                    st.markdown(p['learning_outcomes'])

                    if p['suggested_extensions']:
                        st.markdown(f"**Suggested Extensions:** {p['suggested_extensions']}")

                with col_right:
                    st.markdown("##### 🏷️ Required Skills:")
                    if p['skills']:
                        for sk in p['skills']:
                            st.markdown(f"- `{sk}`")
                    else:
                        st.markdown("Multi-disciplinary stack")

                    st.markdown("---")
                    if st.button("🗺️ Build Career Roadmap", key=f"proj_rd_{p['project_id']}", use_container_width=True):
                        st.session_state["target_career_id"] = p["career_id"]
                        st.session_state["current_page"] = "Personalized 8-Stage Roadmap"
                        st.rerun()

                    if st.button("📊 View Skill Gap", key=f"proj_gap_{p['project_id']}", use_container_width=True):
                        st.session_state["target_career_id"] = p["career_id"]
                        st.session_state["current_page"] = "Skill Gap Analyzer"
                        st.rerun()
