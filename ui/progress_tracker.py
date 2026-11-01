# ui/progress_tracker.py
"""
Student Progress Tracker View.
Visual progress dashboards, readiness gauges, milestone checklist updates,
and skill acquisition evolution over time.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Career, Student, StudentProgress
from services.skill_gap_service import SkillGapService
from services.student_service import StudentService

def render_progress_tracker():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">📈 Student Progress Tracker</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Track your journey toward career readiness: monitor acquired skills, stage milestone completions, and overall qualification percentage.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        all_careers = session.query(Career).order_by(Career.title).all()
        career_titles = [c.title for c in all_careers]
        career_map = {c.title: c.career_id for c in all_careers}

        target_id = st.session_state.get("target_career_id", all_careers[0].career_id if all_careers else 1)
        def_idx = 0
        for idx, c in enumerate(all_careers):
            if c.career_id == target_id:
                def_idx = idx
                break

        col_c, col_dummy = st.columns([2.5, 1])
        with col_c:
            selected_title = st.selectbox("Tracking Progress for Target Career:", career_titles, index=def_idx)
        career_id = career_map[selected_title]
        st.session_state["target_career_id"] = career_id

        # Compute current readiness
        student_profile = {
            "skills": st.session_state.get("student_skills", {"Python": "Intermediate"}),
            "weekly_learning_hours": st.session_state.get("weekly_hours", 15)
        }

        gap = SkillGapService.analyze_gap(session, career_id, student_profile)
        readiness = gap["readiness_percentage"]

        completed_stages = st.session_state.get("completed_stages", set())
        completed_projects_count = st.session_state.get("completed_projects_count", 0)

        # Overview Gauges & Metrics
        color = "#10b981" if readiness >= 75 else ("#38bdf8" if readiness >= 50 else "#f59e0b")

        st.markdown(f"""
        <div style="background: rgba(30, 27, 75, 0.45); border: 1px solid rgba(139, 92, 246, 0.25); border-left: 6px solid {color}; padding: 1.4rem; border-radius: 12px; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="color: #ffffff; margin: 0; font-size: 1.35rem;">{gap['title']} Readiness Progress</h3>
                    <div style="color: #c4b5fd; font-size: 0.9rem;">{gap['category_name']} • Required Study: ~{gap['estimated_hours_needed']} hrs remaining</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.2rem; font-weight: 800; color: {color};">{readiness}%</div>
                    <div style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase;">Overall Readiness</div>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <div style="background: rgba(255,255,255,0.1); border-radius: 8px; height: 12px; overflow: hidden;">
                    <div style="background: {color}; width: {readiness}%; height: 100%; border-radius: 8px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Technical Skills Met", f"{gap['acquired_count']} / {gap['total_skills_count']}", f"{int((gap['acquired_count']/gap['total_skills_count'])*100) if gap['total_skills_count'] else 0}%")
        with m2:
            st.metric("Milestone Stages Done", f"{len(completed_stages)} / 8", f"{int(len(completed_stages)/8*100)}%")
        with m3:
            st.metric("Projects Finished", f"{completed_projects_count}", "Portfolio Capstones")
        with m4:
            st.metric("Estimated Timeline", f"{gap['estimated_weeks_needed']} Wks", f"~{gap['estimated_months_needed']} Months")

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # Milestone Checklist Updates
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.subheader("🎯 Active Milestones Checklist")
            st.markdown("Check off stages as you complete tutorials, projects, and assessments:")

            stage_names = [
                (1, "Stage 1: Foundational Prerequisites & Environment Setup"),
                (2, "Stage 2: Core Technical Frameworks & Libraries"),
                (3, "Stage 3: Data Persistence, APIs & Architecture"),
                (4, "Stage 4: Intermediate Architecture & Clean Engineering"),
                (5, "Stage 5: Advanced Domain Specialization & Performance"),
                (6, "Stage 6: Full-Scale Capstone Portfolio Project"),
                (7, "Stage 7: Containerization, CI/CD & Cloud Deployment"),
                (8, "Stage 8: Placement Readiness, Interview Prep & System Design")
            ]

            for s_id, s_title in stage_names:
                done = s_id in completed_stages
                chk = st.checkbox(s_title, value=done, key=f"prog_stg_{s_id}")
                if chk != done:
                    if chk:
                        completed_stages.add(s_id)
                    else:
                        completed_stages.discard(s_id)
                    st.session_state["completed_stages"] = completed_stages
                    st.rerun()

        with col_m2:
            st.subheader("📁 Project Completions")
            st.markdown("Record your finished capstone implementations:")

            completed_projects_count = st.number_input(
                "Completed Portfolio Projects count:",
                min_value=0,
                max_value=20,
                value=int(st.session_state.get("completed_projects_count", 0)),
                step=1
            )
            st.session_state["completed_projects_count"] = completed_projects_count

            st.markdown("##### 💡 Next Action Items:")
            if gap["high_priority_missing"]:
                for s in gap["high_priority_missing"][:3]:
                    st.warning(f"Prioritize learning essential skill: **{s['name']}**")
            elif gap["proficiency_upgrades"]:
                for u in gap["proficiency_upgrades"][:2]:
                    st.info(f"Deepen proficiency in **{u['name']}** to `{u['target_level']}`")
            else:
                st.success("All technical requirements satisfied! Proceed to Stage 8 Interview Preparation.")

            # Database persistence button
            student_id = st.session_state.get("student_id")
            if student_id:
                if st.button("💾 Persist Progress in Database", use_container_width=True):
                    StudentService.update_progress(
                        session=session,
                        student_id=student_id,
                        career_id=career_id,
                        readiness_pct=readiness,
                        completed_skills=gap["acquired_count"],
                        total_skills=gap["total_skills_count"],
                        completed_projects=completed_projects_count,
                        milestones_done=len(completed_stages)
                    )
                    st.success("✓ Progress snapshot saved into database!")
            else:
                st.caption("ℹ️ Save your profile in 'My Profile & Skills' to enable permanent database progress snapshots.")
