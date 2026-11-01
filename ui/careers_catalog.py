# ui/careers_catalog.py
"""
Career Knowledge Base View.
Search and browse 505 specialized career profiles across 50 career families.
Displays complete daily responsibilities, essential skills, education, certifications,
and progression ladders.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Career, CareerCategory

def render_careers_catalog():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">💼 Career Knowledge Base</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Explore comprehensive, verified profiles for 500+ specialized career paths across 50 engineering families.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        f_c1, f_c2, f_c3, f_c4 = st.columns([2, 1.5, 1, 1])

        with f_c1:
            search_query = st.text_input("🔍 Search careers by title, keyword, or duty:", placeholder="e.g. AI Scientist, Cloud Security, Blockchain, SRE...")

        with f_c2:
            all_fams = [c.name for c in session.query(CareerCategory.name).order_by(CareerCategory.name).all()]
            # Pre-select if forwarded from home
            def_idx = 0
            filter_cat_id = st.session_state.get("filter_category_id")
            if filter_cat_id:
                cat_obj = session.query(CareerCategory).filter_by(category_id=filter_cat_id).first()
                if cat_obj and cat_obj.name in all_fams:
                    def_idx = all_fams.index(cat_obj.name) + 1
                    # reset filter
                    st.session_state["filter_category_id"] = None

            selected_fam = st.selectbox("Career Family:", ["All 50 Families"] + all_fams, index=def_idx)

        with f_c3:
            selected_suit = st.selectbox("Entry Suitability:", ["All", "High", "Moderate", "Low", "Experienced"])

        with f_c4:
            selected_diff = st.selectbox("Difficulty:", ["All", "Beginner", "Intermediate", "Advanced"])

        # Construct query
        query = session.query(Career).join(CareerCategory)
        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(
                (Career.title.ilike(term)) |
                (Career.description.ilike(term)) |
                (Career.daily_responsibilities.ilike(term)) |
                (Career.subcategory.ilike(term))
            )
        if selected_fam != "All 50 Families":
            query = query.filter(CareerCategory.name == selected_fam)
        if selected_suit != "All":
            query = query.filter(Career.entry_level_suitability.ilike(f"%{selected_suit}%"))
        if selected_diff != "All":
            query = query.filter(Career.difficulty_level.ilike(f"%{selected_diff}%"))

        total_careers = query.count()
        st.markdown(f"<div style='color: #a5b4fc; margin-bottom: 1rem;'>Showing <strong>{min(total_careers, 30)}</strong> of <strong>{total_careers}</strong> careers:</div>", unsafe_allow_html=True)

        careers = query.limit(30).all()

        for c in careers:
            with st.expander(f"📌 {c.title} ({c.category.name} | Suitability: {c.entry_level_suitability})", expanded=False):
                col_left, col_right = st.columns([2.2, 1])

                with col_left:
                    st.markdown(f"**Subcategory:** `{c.subcategory}` | **Difficulty:** `{c.difficulty_level}`")
                    st.markdown(f"**Overview:** {c.description}")
                    st.markdown(f"**Daily Responsibilities:** {c.daily_responsibilities}")
                    st.markdown(f"**Educational Prerequisites:** {c.required_education} *(Preferred: {c.preferred_education})*")
                    st.markdown(f"**Relevant Branches:** `{c.relevant_branches}`")
                    st.markdown(f"**Industry Sectors:** {c.industry_sectors}")
                    st.markdown(f"**Recommended Certifications:** {c.recommended_certifications}")
                    st.markdown(f"**Career Ladder:** `{c.career_progression}`")

                with col_right:
                    st.markdown("##### 🔑 Essential Skills (70%):")
                    ess = [cs.skill.name for cs in c.skills if cs.skill_type == "essential"]
                    st.markdown(", ".join(ess) if ess else "Not specified")

                    st.markdown("##### 💡 Preferred Skills (20%):")
                    pref = [cs.skill.name for cs in c.skills if cs.skill_type == "preferred"]
                    st.markdown(", ".join(pref) if pref else "None")

                    st.markdown("##### 🌟 Soft Skills:")
                    st.markdown(c.soft_skills or "Communication, problem solving")

                    st.markdown("---")
                    if st.button("📊 Analyze Skill Gap", key=f"gap_btn_{c.career_id}", use_container_width=True):
                        st.session_state["target_career_id"] = c.career_id
                        st.session_state["current_page"] = "Skill Gap Analyzer"
                        st.rerun()

                    if st.button("🗺️ Build 8-Stage Roadmap", key=f"rd_btn_{c.career_id}", use_container_width=True):
                        st.session_state["target_career_id"] = c.career_id
                        st.session_state["current_page"] = "Personalized 8-Stage Roadmap"
                        st.rerun()
