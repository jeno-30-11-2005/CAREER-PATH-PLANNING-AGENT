# ui/career_plan_view.py
"""
My Career Plan View.
Provides a dedicated, distraction-free view of the active target career,
skill gap analysis, personalized 6-stage roadmap, and practical projects.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Career, TechnicalSkill, AreaOfInterest, CareerPathway
from services.skill_gap_service import SkillGapService
from services.roadmap_service import RoadmapService
from services.project_service import ProjectService
from services.resource_service import ResourceService

def render_career_plan_view():
    st.markdown("""
    <div style="padding: 0.8rem 0 1.2rem;">
        <span class="badge-pill-blue">📋 MY CAREER PLAN</span>
        <h1 style="color: #0f172a; font-size: 2rem; font-weight: 800; margin: 0.4rem 0 0.2rem;">
            My Career Plan
        </h1>
        <p style="color: #64748b; font-size: 1rem; margin-bottom: 0;">
            A friendly step-by-step roadmap and project guide for your target career.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        all_careers = session.query(Career).order_by(Career.title).all()
        career_names = [c.title for c in all_careers]
        career_by_name = {c.title: c.career_id for c in all_careers}

        selected_career_id = st.session_state.get("selected_career_id", all_careers[0].career_id if all_careers else 1)
        curr_career = session.query(Career).filter_by(career_id=selected_career_id).first()
        curr_title = curr_career.title if curr_career else career_names[0]
        curr_desc = curr_career.description if curr_career else ""
        curr_cat = curr_career.category.name if (curr_career and curr_career.category) else "Engineering"

        # Career Selector
        c_sel_col1, c_sel_col2 = st.columns([3, 1])
        with c_sel_col1:
            chosen_title = st.selectbox(
                "Select or Switch Target Career:",
                career_names,
                index=career_names.index(curr_title) if curr_title in career_names else 0
            )
            if career_by_name[chosen_title] != selected_career_id:
                st.session_state["selected_career_id"] = career_by_name[chosen_title]
                st.rerun()

        with c_sel_col2:
            st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)
            weekly_hours = st.slider("Weekly Study Hours:", 5, 40, st.session_state.get("weekly_hours", 15), 1)
            st.session_state["weekly_hours"] = weekly_hours

        # Fetch details
        student_profile_dict = {
            "skills": st.session_state.get("student_skills", {}),
            "interests": st.session_state.get("student_interests", []),
            "academic_branch": st.session_state.get("academic_branch", "CSE"),
            "weekly_learning_hours": weekly_hours
        }

        gap = SkillGapService.analyze_gap(session, selected_career_id, student_profile_dict)
        roadmap = RoadmapService.generate_roadmap(session, selected_career_id, student_profile_dict)
        projects = ProjectService.get_projects_for_career(session, selected_career_id)
        resources = ResourceService.get_resources_for_career(session, selected_career_id)

    # 1. Career Summary Card
    with st.container(border=True):
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span class="badge-pill-purple">{curr_cat}</span>
                <h3 style="color: #0f2926; font-size: 1.4rem; font-weight: 800; margin: 0.3rem 0;">{curr_title}</h3>
                <p style="color: #475569; font-size: 0.95rem; line-height: 1.5; margin: 0 0 0.8rem;">{curr_desc}</p>
            </div>
            <div style="text-align: right;">
                <span class="badge-pill-mint" style="font-size: 1.1rem; font-weight: 800;">{gap['readiness_percentage']}% READINESS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(gap['readiness_percentage'] / 100.0)

    # 2. Roadmap Stages
    st.markdown("<h3 style='color: #0f2926; font-weight: 800; margin: 1.2rem 0 0.6rem;'>6-Stage Execution Roadmap</h3>", unsafe_allow_html=True)
    completed_milestones = set(st.session_state.get("completed_milestones", []))

    for stg in roadmap.get("stages", [])[:6]:
        s_num = stg.get("stage_number") or stg.get("stage", 1)
        s_name = stg.get("stage_name") or stg.get("name", "Foundations")
        is_done = f"{selected_career_id}_stage_{s_num}" in completed_milestones
        border_style = "border: 1px solid #86efac; background: #f0fdf4;" if is_done else "border: 1px solid #e5eee9; background: #ffffff;"
        
        st.markdown(f"""
        <div class="card-coachpro" style="{border_style}; padding: 1.1rem 1.3rem;">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <span class="badge-pill-mint" style="font-size: 0.75rem;">STAGE {s_num}</span>
                    <h4 style="color: #0f2926; font-weight: 800; margin: 0.3rem 0 0.2rem;">{s_name}</h4>
                    <p style="color: #475569; font-size: 0.9rem; margin-bottom: 0.4rem;">{stg['description']}</p>
                </div>
                <div style="text-align: right; min-width: 90px;">
                    <span style="color: #0d9488; font-weight: 700;">~{stg.get('estimated_weeks', 2)} Wks</span>
                </div>
            </div>
            <div style="background: rgba(241, 245, 249, 0.7); padding: 0.6rem 0.8rem; border-radius: 8px; font-size: 0.85rem; color: #334155;">
                <b>🎯 Objective:</b> {stg.get('milestone', 'Complete guided hands-on exercises.')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        m_done = st.checkbox(f"Completed Stage {s_num}", value=is_done, key=f"plan_stg_{selected_career_id}_{s_num}")
        if m_done and not is_done:
            completed_milestones.add(f"{selected_career_id}_stage_{s_num}")
            st.session_state["completed_milestones"] = list(completed_milestones)
            st.rerun()
        elif not m_done and is_done:
            completed_milestones.remove(f"{selected_career_id}_stage_{s_num}")
            st.session_state["completed_milestones"] = list(completed_milestones)
            st.rerun()

    # 3. Quick Projects
    st.markdown("<h3 style='color: #0f2926; font-weight: 800; margin: 1.5rem 0 0.6rem;'>Key Portfolio Projects</h3>", unsafe_allow_html=True)
    if projects:
        for p in projects[:2]:
            st.markdown(f"""
            <div class="card-coachpro">
                <div style="display: flex; justify-content: space-between;">
                    <h4 style="color: #0f2926; font-weight: 800; margin: 0;">{p['title']}</h4>
                    <span class="badge-pill-purple">{p['difficulty']}</span>
                </div>
                <p style="color: #475569; font-size: 0.9rem; margin: 0.4rem 0 0.6rem;">{p['description']}</p>
                <div style="font-size: 0.85rem; color: #334155; background: #f8fafc; padding: 0.6rem 0.8rem; border-radius: 8px;">
                    <b>Tools:</b> {p.get('suggested_technologies', 'Python, Git')} • <b>Deliverable:</b> {p.get('deliverables', 'GitHub Repository')}
                </div>
            </div>
            """, unsafe_allow_html=True)
