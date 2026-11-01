# ui/comparison.py
"""
Career Comparison Engine View.
Enables side-by-side comparison of 2 or 3 career profiles:
- Overlapping common skills vs unique domain requirements
- Educational prerequisites and difficulty levels
- Career progression ladders and student compatibility
Designed with the clean CoachPro light aesthetic.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Career
from services.comparison_service import CareerComparisonService

def render_comparison():
    st.markdown("""
    <div style="margin-bottom: 1.2rem;">
        <h2 style="color: #0f2926; font-weight: 800; font-size: 1.6rem; margin-bottom: 0.2rem;">
            ⚖️ Career Comparison Tool
        </h2>
        <p style="color: #475569; font-size: 0.95rem; margin-bottom: 0;">
            Compare 2 or 3 career pathways side-by-side to understand skill overlaps, educational differences, and career ladders.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        all_careers = session.query(Career).order_by(Career.title).all()
        career_titles = [c.title for c in all_careers]
        career_map = {c.title: c.career_id for c in all_careers}

        c1, c2, c3 = st.columns(3)
        with c1:
            sel_1 = st.selectbox("Select Career 1:", career_titles, index=0)
        with c2:
            sel_2 = st.selectbox("Select Career 2:", career_titles, index=min(1, len(career_titles)-1))
        with c3:
            add_third = st.checkbox("Compare 3rd Career", value=False)
            sel_3 = None
            if add_third:
                sel_3 = st.selectbox("Select Career 3:", career_titles, index=min(2, len(career_titles)-1))

        selected_titles = [sel_1, sel_2]
        if sel_3 and sel_3 not in selected_titles:
            selected_titles.append(sel_3)

        career_ids = [career_map[t] for t in selected_titles]

        # Student profile for compatibility
        student_profile = {
            "skills": st.session_state.get("student_skills", {}),
            "interests": st.session_state.get("student_interests", []),
            "academic_branch": st.session_state.get("academic_branch", "CSE"),
            "weekly_learning_hours": st.session_state.get("weekly_hours", 15)
        }

        try:
            comparison = CareerComparisonService.compare_careers(session, career_ids, student_profile)
        except Exception as e:
            st.error(f"Error loading comparison: {str(e)}")
            return

        # Summary Banner
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2ece7; padding: 1.2rem; border-radius: 14px; margin: 1rem 0; box-shadow: 0 4px 16px rgba(0,0,0,0.02);">
            <div style="color: #0f766e; font-weight: 800; font-size: 1rem; margin-bottom: 0.3rem;">📋 Comparative Overview:</div>
            <div style="color: #334155; font-size: 0.95rem; line-height: 1.5;">{comparison['comparison_summary']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Common Skills Banner
        if comparison["common_essential_skills"]:
            st.markdown(f"""
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 0.8rem 1rem; border-radius: 10px; margin-bottom: 1.2rem;">
                <strong style="color: #15803d;">🔗 Common Shared Skills:</strong>
                <span style="color: #166534; font-weight: 600; margin-left: 0.5rem;">{', '.join(comparison['common_essential_skills'])}</span>
            </div>
            """, unsafe_allow_html=True)

        # Side-by-side columns
        cols = st.columns(len(comparison["careers"]))
        for idx, c in enumerate(comparison["careers"]):
            col = cols[idx]
            compat = c.get("student_compatibility")
            compat_str = f"{compat}%" if compat is not None else "N/A"
            badge_color = "#0d9488" if compat and compat >= 70 else "#6b21a8"

            with col:
                st.markdown(f"""
                <div class="card-coachpro" style="border-top: 5px solid {badge_color}; min-height: 520px;">
                    <h3 style="color: #0f2926; font-size: 1.25rem; margin-top: 0; margin-bottom: 0.2rem;">{c['title']}</h3>
                    <div style="color: #64748b; font-size: 0.85rem; margin-bottom: 0.6rem;">{c['category']} • {c['subcategory']}</div>
                    <div style="background: #ccfbf1; color: #0f766e; border: 1px solid #99f6e4; font-weight: 800; font-size: 0.9rem; padding: 4px 10px; border-radius: 6px; display: inline-block; margin-bottom: 1rem;">
                        Your Fit: {compat_str}
                    </div>
                    <div style="margin-bottom: 0.8rem;">
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 700;">DIFFICULTY:</span><br>
                        <strong style="color: #0f2926;">{c['difficulty_level']}</strong>
                    </div>
                    <div style="margin-bottom: 0.8rem;">
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 700;">ENTRY SUITABILITY:</span><br>
                        <strong style="color: #0f2926;">{c['entry_level_suitability']}</strong>
                    </div>
                    <div style="margin-bottom: 0.8rem;">
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 700;">REQUIRED EDUCATION:</span><br>
                        <strong style="color: #0f2926; font-size: 0.9rem;">{c['required_education']}</strong>
                    </div>
                    <div style="margin-bottom: 0.8rem;">
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 700;">UNIQUE SKILLS NEEDED:</span><br>
                        <span style="color: #b45309; font-weight: 600; font-size: 0.85rem;">{', '.join(c['unique_skills'][:4]) if c['unique_skills'] else 'None'}</span>
                    </div>
                    <div style="margin-bottom: 0.8rem;">
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 700;">CAREER LADDER:</span><br>
                        <span style="color: #475569; font-size: 0.85rem;">{c['career_progression']}</span>
                    </div>
                    <div style="margin-bottom: 0.8rem;">
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 700;">INDUSTRY SECTORS:</span><br>
                        <span style="color: #475569; font-size: 0.85rem;">{c['industry_sectors']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Select {c['title'][:14]}.. as My Target", key=f"comp_select_{c['career_id']}", use_container_width=True, type="primary"):
                    st.session_state["selected_career_id"] = c["career_id"]
                    st.session_state["current_view"] = "Home"
                    st.rerun()
