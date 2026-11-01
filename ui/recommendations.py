# ui/recommendations.py
"""
Career Recommendations Engine View.
Calculates multi-factor explainable career matches:
- 70% Essential Skills
- 20% Preferred Skills
- 10% Additional Skills
- Education and Interest boosts
"""
import streamlit as st
from database.connection import get_db_session
from database.models import TechnicalSkill, AreaOfInterest, CareerCategory
from services.recommendation_service import RecommendationEngine

def render_recommendations():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">🧠 Multi-Factor Career Recommendation Engine</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Discover careers precisely aligned with your technical competencies, academic qualifications, and personal interests.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        # 1. Profile Input Form
        with st.expander("⚙️ Configure Recommendation Inputs & Filters", expanded=True):
            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("##### 1. Technical Skills Inventory")
                all_skills = [s.name for s in session.query(TechnicalSkill.name).order_by(TechnicalSkill.name).all()]
                
                # Pre-populate from session state if available
                current_skills_map = st.session_state.get("student_skills", {})
                preselected_skill_names = [k for k in current_skills_map.keys() if isinstance(k, str) and k in all_skills]

                selected_skill_names = st.multiselect(
                    "Select skills you currently possess:",
                    all_skills,
                    default=preselected_skill_names[:8] if preselected_skill_names else ["Python", "FastAPI", "SQL (PostgreSQL)"]
                )

                st.markdown("##### 2. Academic Background")
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    academic_branch = st.selectbox(
                        "Branch of Study:",
                        ["CSE", "IT", "AI & DS", "ECE", "Electrical", "Mechanical", "Civil", "Mathematics", "Bioinformatics", "Finance", "Other"],
                        index=0
                    )
                with col_b2:
                    edu_level = st.selectbox(
                        "Education Level:",
                        ["Bachelor's", "Master's", "Ph.D.", "Diploma", "Self-Taught"],
                        index=0
                    )

            with col_right:
                st.markdown("##### 3. Areas of Interest")
                all_interests = [i.name for i in session.query(AreaOfInterest.name).order_by(AreaOfInterest.name).all()]
                selected_interests = st.multiselect(
                    "Select your areas of passion:",
                    all_interests,
                    default=["Artificial Intelligence", "Machine Learning & Data Science"] if "Artificial Intelligence" in all_interests else all_interests[:2]
                )

                st.markdown("##### 4. Constraints & Filters")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    all_fams = [c.name for c in session.query(CareerCategory.name).order_by(CareerCategory.name).all()]
                    category_filter = st.selectbox("Filter Family (Optional):", ["All 50 Families"] + all_fams)
                with col_f2:
                    top_k = st.selectbox("Number of Recommendations:", [5, 10, 15, 20], index=1)

            weekly_hours = st.slider("Available Weekly Study Hours:", min_value=5, max_value=40, value=15, step=5)

            cat_id = None
            if category_filter != "All 50 Families":
                cat_obj = session.query(CareerCategory).filter_by(name=category_filter).first()
                if cat_obj:
                    cat_id = cat_obj.category_id

        # Run Recommendation Computation
        student_profile = {
            "skills": {s: "Intermediate" for s in selected_skill_names},
            "interests": selected_interests,
            "academic_branch": academic_branch,
            "education_level": edu_level,
            "weekly_learning_hours": weekly_hours
        }

        # Save to session state
        st.session_state["student_skills"] = student_profile["skills"]
        st.session_state["student_interests"] = selected_interests
        st.session_state["academic_branch"] = academic_branch
        st.session_state["weekly_hours"] = weekly_hours

        recs = RecommendationEngine.get_recommendations(
            session=session,
            student_profile=student_profile,
            top_k=top_k,
            category_id=cat_id
        )

        st.markdown(f"### 🎯 Top {len(recs)} Recommended Career Matches")

        for idx, rec in enumerate(recs, 1):
            score = rec["compatibility_score"]
            badge_color = "#10b981" if score >= 75 else ("#38bdf8" if score >= 55 else "#f59e0b")

            st.markdown(f"""
            <div style="background: rgba(30, 27, 75, 0.45); border: 1px solid rgba(139, 92, 246, 0.25); border-left: 6px solid {badge_color}; padding: 1.4rem; border-radius: 12px; margin-bottom: 1.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div>
                        <span style="color: #94a3b8; font-size: 0.9rem; font-weight: 600;">#{idx} MATCH</span>
                        <h3 style="color: #ffffff; margin: 0.1rem 0; font-size: 1.35rem;">{rec['title']}</h3>
                        <div style="color: #c4b5fd; font-size: 0.85rem;">{rec['category_name']} • Subcategory: {rec['subcategory']}</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {badge_color}22; color: {badge_color}; border: 1px solid {badge_color}; font-weight: 800; font-size: 1.25rem; padding: 6px 16px; border-radius: 8px;">
                            {score}% Match
                        </span>
                    </div>
                </div>
                <div style="color: #e2e8f0; font-size: 0.95rem; margin-bottom: 0.8rem; line-height: 1.5;">
                    {rec['description']}
                </div>
                <div style="background: rgba(15, 23, 42, 0.5); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.8rem; border: 1px solid rgba(139, 92, 246, 0.15);">
                    <div style="color: #38bdf8; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.2rem;">💡 Why this matches:</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">{rec['explanation']}</div>
                </div>
                <div style="display: flex; gap: 1.5rem; color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.8rem;">
                    <span>⚡ <strong>Skills Match:</strong> {rec['skill_score']}%</span>
                    <span>🎯 <strong>Interests Overlap:</strong> {rec['interest_score']}%</span>
                    <span>🎓 <strong>Education Fit:</strong> {rec['education_score']}%</span>
                    <span>📊 <strong>Difficulty:</strong> {rec['difficulty_level']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            rc1, rc2, rc3 = st.columns([1, 1, 2])
            with rc1:
                if st.button("📊 Analyze Skill Gap", key=f"rec_gap_{rec['career_id']}", use_container_width=True):
                    st.session_state["target_career_id"] = rec["career_id"]
                    st.session_state["current_page"] = "Skill Gap Analyzer"
                    st.rerun()
            with rc2:
                if st.button("🗺️ Build Roadmap", key=f"rec_rd_{rec['career_id']}", use_container_width=True):
                    st.session_state["target_career_id"] = rec["career_id"]
                    st.session_state["current_page"] = "Personalized 8-Stage Roadmap"
                    st.rerun()
            with rc3:
                # Skill badges summary
                matched_names = [s["name"] for s in rec["matched_essential_skills"]]
                missing_names = [s["name"] for s in rec["missing_essential_skills"]]
                summary_html = ""
                if matched_names:
                    summary_html += f"<span style='color: #10b981; font-size: 0.85rem;'>✓ Have: {', '.join(matched_names[:3])}</span> "
                if missing_names:
                    summary_html += f"<span style='color: #f87171; font-size: 0.85rem;'>| ✗ Need: {', '.join(missing_names[:2])}</span>"
                st.markdown(summary_html, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)
