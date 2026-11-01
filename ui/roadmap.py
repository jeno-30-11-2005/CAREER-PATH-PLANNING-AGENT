# ui/roadmap.py
"""
Personalized 8-Stage Learning Roadmap View.
Calculates dynamic milestones and timelines based on student's study capacity.
Features an interactive checklist to track student milestone completions.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Career
from services.roadmap_service import RoadmapService

def render_roadmap():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">🗺️ Personalized 8-Stage Learning Roadmap</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            A structured, progressive milestone roadmap guiding you from foundational syntax to portfolio deployment and interview readiness.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        all_careers = session.query(Career).order_by(Career.title).all()
        career_titles = [c.title for c in all_careers]
        career_map = {c.title: c.career_id for c in all_careers}

        target_id = st.session_state.get("target_career_id")
        def_idx = 0
        if target_id:
            for idx, c in enumerate(all_careers):
                if c.career_id == target_id:
                    def_idx = idx
                    break

        col_c, col_w = st.columns([2.5, 1])
        with col_c:
            selected_title = st.selectbox("Target Career for Roadmap:", career_titles, index=def_idx)
        with col_w:
            weekly_hours = st.slider("Weekly Study Hours:", 5, 40, value=st.session_state.get("weekly_hours", 15), step=5)
            st.session_state["weekly_hours"] = weekly_hours

        career_id = career_map[selected_title]
        st.session_state["target_career_id"] = career_id

        student_profile = {
            "weekly_learning_hours": weekly_hours
        }

        roadmap = RoadmapService.generate_roadmap(session, career_id, student_profile)

        # Overview Stats
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Stages", f"{roadmap['total_stages']} Stages", "End-to-End")
        with m2:
            st.metric("Total Effort", f"{roadmap['total_hours']} Hours", f"{weekly_hours} hrs/week")
        with m3:
            st.metric("Estimated Weeks", f"{roadmap['estimated_total_weeks']} Weeks", f"~{roadmap['estimated_total_months']} Months")
        with m4:
            st.metric("Difficulty", roadmap['difficulty_level'], roadmap['category_name'])

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # Checkbox state tracking
        completed_stages = st.session_state.get("completed_stages", set())

        # Render 8 stages
        for stage in roadmap["stages"]:
            s_num = stage["stage_number"]
            is_done = s_num in completed_stages

            status_badge = "✅ COMPLETED" if is_done else f"⏳ ~{stage['estimated_weeks']} WEEKS"
            status_color = "#10b981" if is_done else "#8b5cf6"

            st.markdown(f"""
            <div style="background: rgba(30, 27, 75, 0.4); border: 1px solid {'#10b981' if is_done else 'rgba(139, 92, 246, 0.25)'}; padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; border-left: 6px solid {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <div>
                        <span style="color: {status_color}; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;">STAGE {s_num}</span>
                        <h4 style="color: #ffffff; margin: 0.1rem 0; font-size: 1.15rem;">{stage['stage_name']}</h4>
                    </div>
                    <div>
                        <span style="background: {status_color}22; color: {status_color}; border: 1px solid {status_color}; font-weight: 700; font-size: 0.8rem; padding: 4px 10px; border-radius: 6px;">
                            {status_badge} ({stage['estimated_hours']} hrs)
                        </span>
                    </div>
                </div>
                <div style="color: #c4b5fd; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.3rem;">
                    📚 Focus Topic: {stage['topic_title']}
                </div>
                <div style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.6rem;">
                    {stage['description']}
                </div>
                <div style="background: rgba(15, 23, 42, 0.5); padding: 0.6rem 0.9rem; border-radius: 6px; border: 1px solid rgba(139, 92, 246, 0.15);">
                    <strong style="color: #38bdf8; font-size: 0.85rem;">🏆 Milestone Deliverable:</strong>
                    <span style="color: #e2e8f0; font-size: 0.85rem; margin-left: 0.4rem;">{stage['milestone']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            check = st.checkbox(
                f"Mark Stage {s_num} as Completed",
                value=is_done,
                key=f"stage_chk_{career_id}_{s_num}"
            )
            if check != is_done:
                if check:
                    completed_stages.add(s_num)
                else:
                    completed_stages.discard(s_num)
                st.session_state["completed_stages"] = completed_stages
                st.rerun()

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)
        progress_val = len(completed_stages) / 8.0
        st.markdown(f"##### 📈 Overall Roadmap Progress: {int(progress_val * 100)}% ({len(completed_stages)} / 8 Stages Complete)")
        st.progress(progress_val)
