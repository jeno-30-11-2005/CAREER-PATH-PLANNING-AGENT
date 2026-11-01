# ui/skills_explorer.py
"""
Technical Skills Explorer View.
Searchable, filterable catalog across all 1,511 technical skills and 90 domains.
Allows students to inspect skill details, aliases, prerequisites, and add directly
to their personal skill inventory.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import TechnicalSkill, SkillCategory, CareerSkill

def render_skills_explorer():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">⚡ Technical Skills Explorer</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Explore our curated knowledge base of 1,500+ technical skills spanning 90 specialized technology domains.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        # Filter controls
        f_c1, f_c2, f_c3, f_c4 = st.columns([2, 1.5, 1, 1])

        with f_c1:
            search_query = st.text_input("🔍 Search skills, tools, or concepts:", placeholder="e.g. Python, Docker, PyTorch, Kubernetes...")

        with f_c2:
            all_cats = [c.name for c in session.query(SkillCategory.name).order_by(SkillCategory.name).all()]
            selected_cat = st.selectbox("Filter Domain / Category:", ["All Domains"] + all_cats)

        with f_c3:
            selected_diff = st.selectbox("Difficulty:", ["All Levels", "Beginner", "Intermediate", "Advanced"])

        with f_c4:
            selected_priority = st.selectbox("Priority:", ["All Priorities", "High", "Medium", "Core"])

        # Construct query
        query = session.query(TechnicalSkill).join(SkillCategory).filter(TechnicalSkill.is_active == True)

        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(
                (TechnicalSkill.name.ilike(term)) |
                (TechnicalSkill.description.ilike(term)) |
                (TechnicalSkill.subcategory.ilike(term))
            )
        if selected_cat != "All Domains":
            query = query.filter(SkillCategory.name == selected_cat)
        if selected_diff != "All Levels":
            query = query.filter(TechnicalSkill.difficulty_level.ilike(f"%{selected_diff}%"))
        if selected_priority != "All Priorities":
            query = query.filter(TechnicalSkill.learning_priority.ilike(f"%{selected_priority}%"))

        total_results = query.count()
        st.markdown(f"<div style='color: #a5b4fc; margin-bottom: 1rem;'>Showing <strong>{min(total_results, 50)}</strong> of <strong>{total_results:,}</strong> matching technical skills:</div>", unsafe_allow_html=True)

        skills = query.limit(50).all()

        # Display skills in responsive cards / expanders
        student_skills = st.session_state.get("student_skills", {})

        for sk in skills:
            with st.expander(f"🔹 {sk.name} ({sk.category.name} | {sk.difficulty_level})", expanded=False):
                s_c1, s_c2 = st.columns([2.5, 1])
                with s_c1:
                    st.markdown(f"**Description:** {sk.description}")
                    st.markdown(f"**Subcategory:** `{sk.subcategory}` | **Difficulty:** `{sk.difficulty_level}` | **Priority:** `{sk.learning_priority}`")
                    
                    # Show associated career roles
                    careers = session.query(CareerSkill).filter_by(skill_id=sk.skill_id).limit(4).all()
                    if careers:
                        career_titles = [cs.career.title for cs in careers if cs.career]
                        st.markdown(f"**Relevant Careers:** {', '.join(career_titles)}")

                with s_c2:
                    st.markdown("##### 📌 My Inventory")
                    is_acquired = sk.skill_id in student_skills or sk.name in student_skills
                    current_prof = student_skills.get(sk.skill_id) or student_skills.get(sk.name) or "Intermediate"

                    if is_acquired:
                        st.success(f"✓ Acquired ({current_prof})")
                        if st.button("Remove from My Skills", key=f"rem_{sk.skill_id}"):
                            if sk.skill_id in student_skills:
                                del student_skills[sk.skill_id]
                            if sk.name in student_skills:
                                del student_skills[sk.name]
                            st.session_state["student_skills"] = student_skills
                            st.rerun()
                    else:
                        new_prof = st.selectbox(
                            "Proficiency:",
                            ["Beginner", "Intermediate", "Advanced", "Expert"],
                            index=1,
                            key=f"prof_sel_{sk.skill_id}"
                        )
                        if st.button("➕ Add to My Skills", key=f"add_{sk.skill_id}", use_container_width=True):
                            student_skills[sk.skill_id] = new_prof
                            st.session_state["student_skills"] = student_skills
                            st.success(f"Added {sk.name}!")
                            st.rerun()
