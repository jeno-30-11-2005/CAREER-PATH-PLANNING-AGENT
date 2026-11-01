# ui/skill_gap.py
"""
Skill Gap Analyzer View.
Detailed competency delta breakdown for any target career:
- Readiness percentage
- High, Medium, Low priority missing competencies
- Required proficiency upgrades
- Estimated study hours & timeline
- Actionable bridging milestones
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Career
from services.skill_gap_service import SkillGapService

def render_skill_gap():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">📊 Skill Gap Analysis Engine</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Inspect the exact competencies required for your target career, identify missing prerequisites, and see your estimated time to readiness.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        all_careers = session.query(Career).order_by(Career.title).all()
        career_titles = [c.title for c in all_careers]
        career_map = {c.title: c.career_id for c in all_careers}

        # Determine default index
        target_id = st.session_state.get("target_career_id")
        def_idx = 0
        if target_id:
            for idx, c in enumerate(all_careers):
                if c.career_id == target_id:
                    def_idx = idx
                    break

        col_sel, col_hours = st.columns([2.5, 1])
        with col_sel:
            selected_career_title = st.selectbox(
                "Select Target Career Role to Analyze:",
                career_titles,
                index=def_idx
            )
        with col_hours:
            weekly_hours = st.slider("Weekly Study Hours:", 5, 40, value=st.session_state.get("weekly_hours", 15), step=5)
            st.session_state["weekly_hours"] = weekly_hours

        target_career_id = career_map[selected_career_title]
        st.session_state["target_career_id"] = target_career_id

        # Student profile
        student_profile = {
            "skills": st.session_state.get("student_skills", {"Python": "Intermediate"}),
            "weekly_learning_hours": weekly_hours
        }

        gap = SkillGapService.analyze_gap(session, target_career_id, student_profile)

        # Overview Banner
        readiness = gap["readiness_percentage"]
        color = "#10b981" if readiness >= 75 else ("#38bdf8" if readiness >= 50 else "#f59e0b")

        st.markdown(f"""
        <div style="background: rgba(30, 27, 75, 0.45); border: 1px solid rgba(139, 92, 246, 0.25); border-left: 6px solid {color}; padding: 1.4rem; border-radius: 12px; margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="color: #ffffff; margin: 0; font-size: 1.4rem;">{gap['title']}</h3>
                    <div style="color: #c4b5fd; font-size: 0.9rem;">Family: {gap['category_name']} • Subcategory: {gap['subcategory']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.2rem; font-weight: 800; color: {color};">{readiness}%</div>
                    <div style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase;">Readiness Score</div>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <div style="background: rgba(255,255,255,0.1); border-radius: 8px; height: 10px; overflow: hidden;">
                    <div style="background: {color}; width: {readiness}%; height: 100%; border-radius: 8px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Metrics row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Acquired Skills", f"{gap['acquired_count']} / {gap['total_skills_count']}", "Competent")
        with m2:
            st.metric("Missing Skills", f"{gap['missing_count']}", "To Acquire")
        with m3:
            st.metric("Proficiency Upgrades", f"{gap['upgrades_needed_count']}", "Advance Level")
        with m4:
            st.metric("Estimated Time", f"{gap['estimated_weeks_needed']} Wks", f"{gap['estimated_hours_needed']} hrs @ {weekly_hours}h/wk")

        # Actionable Advice Card
        if gap["actionable_advice"]:
            st.markdown("#### 🎯 Actionable Study Strategy")
            for advice in gap["actionable_advice"]:
                st.info(advice)

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # Categorized Skill Breakdowns
        t1, t2, t3, t4 = st.tabs([
            f"🚨 High Priority Missing ({len(gap['high_priority_missing'])})",
            f"⚠️ Medium Priority ({len(gap['medium_priority_missing'])})",
            f"🔄 Proficiency Upgrades ({len(gap['proficiency_upgrades'])})",
            f"✅ Acquired Skills ({gap['acquired_count']})"
        ])

        with t1:
            if gap["high_priority_missing"]:
                st.markdown("<p style='color: #f87171;'>These are <strong>Essential Skills (70% weight)</strong> that you currently do not possess:</p>", unsafe_allow_html=True)
                for s in gap["high_priority_missing"]:
                    st.markdown(f"""
                    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 0.8rem 1.2rem; border-radius: 8px; margin-bottom: 0.6rem;">
                        <strong style="color: #fca5a5; font-size: 1.05rem;">{s['name']}</strong>
                        <span style="color: #cbd5e1; font-size: 0.85rem; margin-left: 1rem;">Target Level: <strong>{s['required_proficiency']}</strong> | Est: ~{s.get('estimated_hours', 70)} hrs</span>
                        <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.3rem;">{s['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("🎉 Outstanding! You already possess all essential skills for this career!")

        with t2:
            if gap["medium_priority_missing"]:
                st.markdown("<p style='color: #fbbf24;'>Preferred or secondary skills that provide a competitive hiring edge:</p>", unsafe_allow_html=True)
                for s in gap["medium_priority_missing"]:
                    st.markdown(f"""
                    <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); padding: 0.8rem 1.2rem; border-radius: 8px; margin-bottom: 0.6rem;">
                        <strong style="color: #fde68a; font-size: 1.05rem;">{s['name']}</strong>
                        <span style="color: #cbd5e1; font-size: 0.85rem; margin-left: 1rem;">Target Level: <strong>{s.get('required_proficiency', 'Intermediate')}</strong></span>
                        <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.3rem;">{s.get('description', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No medium priority gaps detected.")

        with t3:
            if gap["proficiency_upgrades"]:
                st.markdown("<p style='color: #38bdf8;'>Skills you already know, but need to advance to meet industry standards:</p>", unsafe_allow_html=True)
                for u in gap["proficiency_upgrades"]:
                    st.markdown(f"""
                    <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); padding: 0.8rem 1.2rem; border-radius: 8px; margin-bottom: 0.6rem;">
                        <strong style="color: #bae6fd; font-size: 1.05rem;">{u['name']}</strong>
                        <span style="color: #e2e8f0; font-size: 0.85rem; margin-left: 1rem;">Current: <span style="color: #f87171;">{u['current_level']}</span> ➔ Target: <span style="color: #34d399;">{u['target_level']}</span> (Est: ~{u['estimated_hours']} hrs)</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✓ All your acquired skills meet or exceed the required proficiency levels!")

        with t4:
            all_acquired = gap["acquired_essential"] + gap["acquired_preferred"] + gap["acquired_additional"]
            if all_acquired:
                for a in all_acquired:
                    st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 0.6rem 1rem; border-radius: 8px; margin-bottom: 0.4rem;">
                        <strong style="color: #6ee7b7;">✓ {a['name']}</strong>
                        <span style="color: #94a3b8; font-size: 0.85rem; margin-left: 0.8rem;">Your Level: {a['current_proficiency']} | Required: {a['required_proficiency']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No matching acquired skills detected yet. Add skills in 'My Profile & Skills'!")

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # Direct CTA
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("🗺️ Build Personalized 8-Stage Roadmap for this Career", type="primary", use_container_width=True):
                st.session_state["target_career_id"] = target_career_id
                st.session_state["current_page"] = "Personalized 8-Stage Roadmap"
                st.rerun()
        with btn_col2:
            if st.button("📁 View Practical Portfolio Projects for this Role", use_container_width=True):
                st.session_state["target_career_id"] = target_career_id
                st.session_state["current_page"] = "Practical Portfolio Projects"
                st.rerun()
