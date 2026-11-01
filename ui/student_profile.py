# ui/student_profile.py
"""
Student Profile & Skill Inventory View.
Manage personal information, academic branch, target career aspirations,
and an active inventory of technical skills with proficiency levels.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import (
    Student, TechnicalSkill, AreaOfInterest, Career
)
from services.student_service import StudentService

def render_student_profile():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">👤 Student Profile & Skill Inventory</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Keep your academic background, target aspirations, and verified skill inventory updated to power intelligent recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        # Pre-cache careers, skills, interests
        all_careers = session.query(Career).order_by(Career.title).all()
        career_titles = ["None / Undecided"] + [c.title for c in all_careers]
        career_map = {c.title: c.career_id for c in all_careers}

        all_skills = session.query(TechnicalSkill).order_by(TechnicalSkill.name).all()
        skill_names = [s.name for s in all_skills]
        skill_name_to_id = {s.name: s.skill_id for s in all_skills}
        skill_id_to_name = {s.skill_id: s.name for s in all_skills}

        all_interests = session.query(AreaOfInterest).order_by(AreaOfInterest.name).all()
        interest_names = [i.name for i in all_interests]
        interest_name_to_id = {i.name: i.interest_id for i in all_interests}
        interest_id_to_name = {i.interest_id: i.name for i in all_interests}

        # 1. Academic & Personal Information
        st.subheader("1. Academic & Personal Information")
        col_p1, col_p2 = st.columns(2)

        with col_p1:
            full_name = st.text_input("Full Name:", value=st.session_state.get("full_name", "Student Explorer"))
            email = st.text_input("Email Address:", value=st.session_state.get("email", "student@university.edu"))
            academic_branch = st.selectbox(
                "Academic Branch / Major:",
                ["CSE", "IT", "AI & DS", "ECE", "Electrical", "Mechanical", "Civil", "Mathematics", "Bioinformatics", "Finance", "Other"],
                index=0
            )

        with col_p2:
            edu_level = st.selectbox(
                "Current Education Level:",
                ["Bachelor's", "Master's", "Ph.D.", "Diploma", "Self-Taught"],
                index=0
            )
            current_year = st.selectbox("Current Academic Year:", [1, 2, 3, 4, 5], index=2)
            weekly_hours = st.slider("Available Weekly Study Hours:", 5, 40, value=st.session_state.get("weekly_hours", 15), step=5)

        # Target Career Goal
        def_target_idx = 0
        current_target_id = st.session_state.get("target_career_id")
        if current_target_id:
            c_obj = session.query(Career).filter_by(career_id=current_target_id).first()
            if c_obj and c_obj.title in career_titles:
                def_target_idx = career_titles.index(c_obj.title)

        selected_target_career = st.selectbox("Target Career Aspiration (Optional):", career_titles, index=def_target_idx)
        chosen_target_id = career_map.get(selected_target_career)

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 2. Technical Skills Inventory
        st.subheader("2. My Technical Skills Inventory")
        student_skills = st.session_state.get("student_skills", {})

        # Normalize keys to name for easy UI rendering
        normalized_skills = {}
        for k, v in student_skills.items():
            if isinstance(k, int) and k in skill_id_to_name:
                normalized_skills[skill_id_to_name[k]] = v
            else:
                normalized_skills[str(k)] = v

        col_add_s, col_add_p, col_add_b = st.columns([2.5, 1.2, 1])
        with col_add_s:
            new_skill_name = st.selectbox("Select a technical skill to add:", [""] + skill_names, index=0)
        with col_add_p:
            new_skill_prof = st.selectbox("Proficiency:", ["Beginner", "Intermediate", "Advanced", "Expert"], index=1)
        with col_add_b:
            st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
            if st.button("➕ Add Skill", use_container_width=True):
                if new_skill_name:
                    normalized_skills[new_skill_name] = new_skill_prof
                    st.session_state["student_skills"] = normalized_skills
                    st.success(f"Added {new_skill_name} ({new_skill_prof})")
                    st.rerun()

        # Custom Skill Add
        with st.expander("➕ Can't find your skill? Add a custom skill"):
            cust_col1, cust_col2, cust_col3 = st.columns([2.5, 1.2, 1])
            with cust_col1:
                custom_name = st.text_input("Custom Skill Name:", placeholder="e.g. Mojo, Langfuse, Zig...")
            with cust_col2:
                custom_prof = st.selectbox("Custom Proficiency:", ["Beginner", "Intermediate", "Advanced", "Expert"], index=1, key="cust_prof")
            with cust_col3:
                st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
                if st.button("Add Custom", use_container_width=True):
                    if custom_name.strip():
                        normalized_skills[custom_name.strip()] = custom_prof
                        st.session_state["student_skills"] = normalized_skills
                        st.success(f"Added custom skill {custom_name.strip()}!")
                        st.rerun()

        # Display Current Active Skills Table / Editor
        st.markdown(f"<div style='color: #a5b4fc; margin: 1rem 0 0.5rem;'>You currently have <strong>{len(normalized_skills)}</strong> active skills in your profile:</div>", unsafe_allow_html=True)

        if normalized_skills:
            for s_name, s_prof in list(normalized_skills.items()):
                c_s1, c_s2, c_s3 = st.columns([2.5, 1.2, 1])
                with c_s1:
                    st.markdown(f"**{s_name}**")
                with c_s2:
                    st.markdown(f"`{s_prof}`")
                with c_s3:
                    if st.button("🗑️ Remove", key=f"del_sk_{s_name}"):
                        del normalized_skills[s_name]
                        st.session_state["student_skills"] = normalized_skills
                        st.rerun()
        else:
            st.info("No skills added yet. Select a skill above and click 'Add Skill'.")

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 3. Areas of Interest
        st.subheader("3. My Areas of Interest")
        student_interests = st.session_state.get("student_interests", [])
        
        # Normalize interest identifiers
        normalized_interests = []
        for item in student_interests:
            if isinstance(item, int) and item in interest_id_to_name:
                normalized_interests.append(interest_id_to_name[item])
            elif isinstance(item, str) and item in interest_names:
                normalized_interests.append(item)

        selected_user_interests = st.multiselect(
            "Select your fields of interest and domain passion:",
            interest_names,
            default=normalized_interests if normalized_interests else (interest_names[:2] if interest_names else [])
        )
        st.session_state["student_interests"] = selected_user_interests

        st.markdown("<hr style='border: 1px solid rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 4. Save to Database
        if st.button("💾 Save Profile & Synchronize Database", type="primary", use_container_width=True):
            try:
                # Update student
                student = StudentService.create_or_update_student(
                    session=session,
                    full_name=full_name,
                    email=email,
                    academic_branch=academic_branch,
                    education_level=edu_level,
                    current_year=current_year,
                    weekly_hours=weekly_hours,
                    target_career_id=chosen_target_id
                )

                # Update skills in DB
                skills_to_persist = {}
                for s_name, s_prof in normalized_skills.items():
                    s_id = skill_name_to_id.get(s_name)
                    if s_id:
                        skills_to_persist[s_id] = s_prof

                StudentService.set_student_skills(session, student.student_id, skills_to_persist)

                # Update interests in DB
                interest_ids_to_persist = [
                    interest_name_to_id[name] for name in selected_user_interests if name in interest_name_to_id
                ]
                StudentService.set_student_interests(session, student.student_id, interest_ids_to_persist)

                # Sync local session state
                st.session_state["student_id"] = student.student_id
                st.session_state["full_name"] = full_name
                st.session_state["email"] = email
                st.session_state["academic_branch"] = academic_branch
                st.session_state["weekly_hours"] = weekly_hours
                if chosen_target_id:
                    st.session_state["target_career_id"] = chosen_target_id

                st.success(f"✓ Profile successfully updated in database for {full_name} ({len(skills_to_persist)} skills, {len(interest_ids_to_persist)} interests)!")
            except Exception as e:
                st.error(f"Error saving profile: {str(e)}")
