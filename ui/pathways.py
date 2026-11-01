# ui/pathways.py
"""
Career Transition & Progression Pathways View.
Explore 450+ realistic career ladders, vertical promotions, and lateral cross-domain transitions:
- Starting role to next destination role
- Required delta skills to make the jump
- Estimated duration in months and transition preparation guidelines
"""
import streamlit as st
from database.connection import get_db_session
from database.models import CareerPathway, Career

def render_pathways():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">🪜 Career Progression & Transition Pathways</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Discover verified career growth trajectories, vertical promotions, and lateral pivots across 50 engineering domains.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        f_c1, f_c2 = st.columns([1.5, 1])

        with f_c1:
            all_types = [row[0] for row in session.query(CareerPathway.progression_type).distinct().all() if row[0]]
            selected_type = st.selectbox("Progression Type:", ["All Types"] + all_types)

        with f_c2:
            search_query = st.text_input("🔍 Filter by career keyword:", placeholder="e.g. AI, DevOps, Security, Cloud...")

        query = session.query(CareerPathway).join(Career, CareerPathway.starting_career_id == Career.career_id)

        if selected_type != "All Types":
            query = query.filter(CareerPathway.progression_type == selected_type)
        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(
                (CareerPathway.required_skills_delta.ilike(term)) |
                (CareerPathway.additional_learning.ilike(term)) |
                (CareerPathway.preparation_guidelines.ilike(term))
            )

        total_pathways = query.count()
        st.markdown(f"<div style='color: #a5b4fc; margin-bottom: 1rem;'>Showing <strong>{min(total_pathways, 40)}</strong> of <strong>{total_pathways}</strong> pathways:</div>", unsafe_allow_html=True)

        pathways = query.limit(40).all()

        for pw in pathways:
            start_title = pw.starting_career.title if pw.starting_career else "Starting Role"
            next_title = pw.next_career.title if pw.next_career else "Target Role"

            badge_color = "#38bdf8" if "Lateral" in pw.progression_type else ("#10b981" if "Vertical" in pw.progression_type else "#8b5cf6")

            with st.expander(f"➔ {start_title}  ➜  {next_title} ({pw.progression_type})", expanded=False):
                st.markdown(f"""
                <div style="background: rgba(30, 27, 75, 0.4); border-left: 4px solid {badge_color}; padding: 1rem; border-radius: 8px; margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <span style="color: {badge_color}; font-weight: 700; font-size: 0.9rem;">{pw.progression_type}</span>
                        <span style="color: #cbd5e1; font-size: 0.85rem;">Estimated Timeline: <strong>{pw.estimated_duration_months} Months</strong></span>
                    </div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">
                        {start_title} <span style="color: #a5b4fc;">➔</span> {next_title}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**Required Competencies Delta:**\n{pw.required_skills_delta}")
                    st.markdown(f"**Additional Recommended Learning:**\n{pw.additional_learning}")
                with col_b:
                    st.markdown(f"**Recommended Transition Projects:**\n{pw.recommended_projects}")
                    st.markdown(f"**Preparation Guidelines:**\n{pw.preparation_guidelines}")

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"Analyze Gap for {next_title[:16]}..", key=f"pw_gap_{pw.pathway_id}"):
                        st.session_state["target_career_id"] = pw.next_career_id
                        st.session_state["current_page"] = "Skill Gap Analyzer"
                        st.rerun()
                with col_btn2:
                    if st.button(f"Build Roadmap for {next_title[:16]}..", key=f"pw_rd_{pw.pathway_id}"):
                        st.session_state["target_career_id"] = pw.next_career_id
                        st.session_state["current_page"] = "Personalized 8-Stage Roadmap"
                        st.rerun()
