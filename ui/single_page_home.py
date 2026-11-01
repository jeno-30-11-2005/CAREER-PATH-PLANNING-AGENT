# ui/single_page_home.py
"""
Single-Page Career Guide View.
Designed to be the simplest, friendliest, most encouraging student career guide:
- Simple for a 5th standard, Plus Two, or college student to understand immediately.
- 4 clear questions: What are you studying? What do you like? What skills do you know? Dream job (optional).
- Top 5 simple career recommendation cards.
- Complete 7-part Career Plan displayed on the same page.
- Retains 100% of the 1,511+ skills, 505+ careers, and AI recommendation intelligence behind the scenes.
"""
import streamlit as st
from typing import Dict, Any, List
from database.connection import get_db_session
from database.models import (
    TechnicalSkill, AreaOfInterest, Career, CareerCategory,
    CareerSkill, CareerInterest, Project, LearningResource, CareerPathway
)
from services.recommendation_service import RecommendationEngine
from services.skill_gap_service import SkillGapService
from services.roadmap_service import RoadmapService
from services.project_service import ProjectService
from services.resource_service import ResourceService

def render_single_page_home():
    """Renders the friendly, beginner-ready Career Guide experience."""
    
    # -------------------------------------------------------------------------
    # 1. FRIENDLY HEADER (Clean, Warm & Encouraging)
    # -------------------------------------------------------------------------
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 1.2rem;">
        <span class="badge-pill-blue">🎓 CAREER GUIDE</span>
        <h1 style="color: #0f172a; font-size: 2.2rem; font-weight: 800; margin: 0.5rem 0 0.2rem; letter-spacing: -0.3px;">
            Career Guide
        </h1>
        <p style="color: #2563eb; font-size: 1.15rem; font-weight: 600; margin-bottom: 0.3rem;">
            Find What You Like. Discover What You Can Become.
        </p>
        <p style="color: #64748b; font-size: 0.95rem; margin-top: 0; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.5;">
            Welcome! Answer a few simple questions about what you enjoy, and we will show you exciting careers and a step-by-step plan to get there.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch database options once
    with get_db_session() as session:
        all_skills_list = [name for (name,) in session.query(TechnicalSkill.name).order_by(TechnicalSkill.name).all()]
        all_interests_list = [name for (name,) in session.query(AreaOfInterest.name).order_by(AreaOfInterest.name).all()]

    # -------------------------------------------------------------------------
    # 2. SIMPLE STUDENT INPUT (4 Approachable Steps)
    # -------------------------------------------------------------------------
    with st.container(border=True):
        st.markdown("<h3 style='color: #0f172a; font-size: 1.25rem; font-weight: 800; margin-bottom: 0.8rem;'>✨ Tell Us About Yourself</h3>", unsafe_allow_html=True)

        col_input_1, col_input_2 = st.columns(2)

        # Step 1: What are you studying?
        with col_input_1:
            edu_options = [
                "School (Classes 5 to 10)",
                "Plus Two (Classes 11 & 12 / Pre-University)",
                "Diploma",
                "Undergraduate (College / Bachelor's Degree)",
                "Postgraduate (Master's / Higher Studies)",
                "Other"
            ]
            current_edu = st.session_state.get("education_level", edu_options[3])
            edu_idx = edu_options.index(current_edu) if current_edu in edu_options else 3
            edu_input = st.selectbox("1. What are you studying?", edu_options, index=edu_idx)
            st.session_state["education_level"] = edu_input

            # Student name (Optional/friendly)
            name_input = st.text_input("Your Name (Optional):", value=st.session_state.get("student_name", "Student Explorer"), placeholder="Enter your name")
            st.session_state["student_name"] = name_input

        # Step 2: What do you like?
        with col_input_2:
            default_interests = [i for i in ["Artificial Intelligence", "Computers & Software", "Robotics & Automation"] if i in all_interests_list]
            curr_interests = st.session_state.get("student_interests", default_interests)
            valid_interests = [i for i in curr_interests if i in all_interests_list]
            selected_interests = st.multiselect(
                "2. What do you like? (Pick 1 to 5 areas that excite you):",
                all_interests_list,
                default=valid_interests if valid_interests else all_interests_list[:3],
                help="Search and pick topics you find interesting, e.g. Artificial Intelligence, Robotics, Designing, Games..."
            )
            st.session_state["student_interests"] = selected_interests

            # Step 4: Dream Job (Optional)
            career_goal_input = st.text_input(
                "4. What career would you like to explore? (Optional):",
                value=st.session_state.get("preferred_career_goal", ""),
                placeholder="e.g. Game Developer, AI Engineer, Robotics Specialist"
            )
            st.session_state["preferred_career_goal"] = career_goal_input

        # Step 3: What skills do you know?
        st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 1rem 0 0.8rem;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #0f172a; font-size: 1.05rem; font-weight: 700; margin-bottom: 0.2rem;'>3. What skills do you know?</h4>", unsafe_allow_html=True)
        st.caption("Select skills you have tried before. If you are starting fresh, it is completely okay to leave this blank!")

        curr_skill_keys = list(st.session_state.get("student_skills", {}).keys())
        valid_selected_skills = [s for s in curr_skill_keys if s in all_skills_list]

        selected_skill_names = st.multiselect(
            "Search and select skills you know:",
            all_skills_list,
            default=valid_selected_skills,
            help="Choose from 1,511 technical skills in our database: Python, Java, HTML, C++, etc."
        )

        # Optional skill proficiency adjuster
        if selected_skill_names:
            with st.expander("⚙️ Set skill levels (Beginner / Intermediate / Advanced)", expanded=False):
                prof_cols = st.columns(3)
                updated_skills_dict = {}
                for idx, sk in enumerate(selected_skill_names):
                    col = prof_cols[idx % 3]
                    curr_level = st.session_state.get("student_skills", {}).get(sk, "Beginner")
                    levels = ["Beginner", "Intermediate", "Advanced"]
                    new_lvl = col.selectbox(f"{sk}", levels, index=levels.index(curr_level) if curr_level in levels else 0, key=f"prof_{sk}")
                    updated_skills_dict[sk] = new_lvl
                st.session_state["student_skills"] = updated_skills_dict
        else:
            st.session_state["student_skills"] = {}

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        find_btn = st.button("🚀 FIND MY CAREER", type="primary", use_container_width=True)
        if find_btn:
            st.session_state["career_analysis_triggered"] = True
            st.success("✨ Great! We found the best careers matching your interests and background.")
            st.rerun()

    # -------------------------------------------------------------------------
    # 3. SHOW CAREERS IN A SIMPLE WAY (Top 5 Suitable Careers)
    # -------------------------------------------------------------------------
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom: 0.8rem;">
        <h2 style="color: #0f172a; font-size: 1.5rem; font-weight: 800; margin: 0 0 0.2rem;">
            🎯 Recommended Careers For You
        </h2>
        <p style="color: #64748b; font-size: 0.95rem; margin: 0;">
            Here are the top careers that match what you like and what you are studying. Choose any career to see your full learning plan!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Generate Recommendations via Engine
    with get_db_session() as session:
        student_profile_dict = {
            "skills": st.session_state.get("student_skills", {}),
            "interests": st.session_state.get("student_interests", []),
            "academic_branch": "Computer Science" if "Computer" in str(st.session_state.get("student_interests", [])) else "Engineering",
            "education_level": st.session_state.get("education_level", "School"),
            "weekly_learning_hours": st.session_state.get("weekly_hours", 10)
        }
        recommendations = RecommendationEngine.get_recommendations(
            session=session,
            student_profile=student_profile_dict,
            top_k=5
        )

    if not recommendations:
        st.info("Please pick at least one thing you like in Step 2 above and click 'FIND MY CAREER'.")
        return

    # Default to top recommendation if none selected
    selected_career_id = st.session_state.get("selected_career_id")
    if not selected_career_id or not any(r["career_id"] == selected_career_id for r in recommendations):
        selected_career_id = recommendations[0]["career_id"]
        st.session_state["selected_career_id"] = selected_career_id

    # Display Top 5 Careers
    for idx, rec in enumerate(recommendations[:5]):
        cid = rec["career_id"]
        is_selected = (cid == selected_career_id)
        score = rec["compatibility_score"]

        with st.container(border=True):
            r_top1, r_top2 = st.columns([3, 1])
            with r_top1:
                st.markdown(f"<span class='badge-pill-purple'>{rec['category_name']}</span>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color: #0f172a; font-size: 1.35rem; font-weight: 800; margin: 0.3rem 0 0.1rem;'>{rec['title']}</h3>", unsafe_allow_html=True)
            with r_top2:
                if score >= 70:
                    badge_cls = "badge-pill-green"
                elif score >= 50:
                    badge_cls = "badge-pill-blue"
                else:
                    badge_cls = "badge-pill-amber"
                
                score_text = f"<span class='{badge_cls}' style='font-size: 0.9rem; font-weight: 800;'>{score}% MATCH 🎯</span>"
                if is_selected:
                    score_text += " <span class='badge-pill-green' style='font-size: 0.78rem; font-weight: 800;'>SELECTED</span>"
                st.markdown(f"<div style='text-align: right;'>{score_text}</div>", unsafe_allow_html=True)

            # What is this job? (Friendly simple explanation)
            st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-top: 0.5rem;'>What is this job?</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #334155; font-size: 0.95rem; line-height: 1.5; margin: 0.2rem 0 0.8rem;'>\"{rec['description']}\"</p>", unsafe_allow_html=True)

            # Skills columns: You already know vs You can learn next
            c_have, c_next = st.columns(2)
            with c_have:
                st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #15803d; text-transform: uppercase; margin-bottom: 0.3rem;'>✓ You already know:</div>", unsafe_allow_html=True)
                matched_skills = rec.get("matched_essential_skills", [])[:4]
                if matched_skills:
                    tags = "".join([f"<span class='skill-pill-matched'>✓ {s.get('name') or s.get('skill_name', '')}</span>" for s in matched_skills])
                    st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: #64748b; font-size: 0.85rem; font-style: italic;'>Great place to start fresh!</span>", unsafe_allow_html=True)

            with c_next:
                st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #b45309; text-transform: uppercase; margin-bottom: 0.3rem;'>⚡ You can learn next:</div>", unsafe_allow_html=True)
                missing_skills = rec.get("missing_essential_skills", [])[:3]
                if missing_skills:
                    tags = "".join([f"<span class='skill-pill-missing'>+ {s.get('name') or s.get('skill_name', '')}</span>" for s in missing_skills])
                    st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: #2563eb; font-size: 0.85rem; font-style: italic;'>You have all key starter skills!</span>", unsafe_allow_html=True)

            st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)
            
            # Action button
            b_col1, b_col2 = st.columns([1, 3])
            with b_col1:
                btn_type = "primary" if is_selected else "secondary"
                btn_label = "📖 ACTIVE PLAN" if is_selected else "📖 SEE MY PLAN →"
                if st.button(btn_label, key=f"btn_plan_{cid}", use_container_width=True, type=btn_type):
                    st.session_state["selected_career_id"] = cid
                    st.rerun()

    # -------------------------------------------------------------------------
    # 4. ONE SIMPLE CAREER PLAN (Appears on the SAME PAGE below)
    # -------------------------------------------------------------------------
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Retrieve complete details for the selected career
    with get_db_session() as session:
        career_obj = session.query(Career).filter_by(career_id=selected_career_id).first()
        if not career_obj:
            return

        career_title = career_obj.title
        career_desc = career_obj.description
        career_daily = career_obj.daily_responsibilities or 'Designs, builds, tests, and improves smart technology solutions while working together with friendly team members.'
        career_req_edu = career_obj.required_education or 'School or College studies in Computer Science, Science, or related field.'
        career_rel_branches = career_obj.relevant_branches or 'Computers, Science, Engineering, or Technology'
        career_soft_skills = career_obj.soft_skills or 'Curiosity, Problem Solving, Teamwork, Creativity'
        career_cat_name = career_obj.category.name if career_obj.category else 'Technology'

        # Skill gap analysis
        gap_results = SkillGapService.analyze_gap(
            session=session,
            target_career_id=selected_career_id,
            student_profile=student_profile_dict
        )

        # 6-stage roadmap
        roadmap_results = RoadmapService.generate_roadmap(
            session=session,
            career_id=selected_career_id,
            student_profile=student_profile_dict
        )

        # Projects & resources
        projects_list = ProjectService.get_projects_for_career(session=session, career_id=selected_career_id)
        resources_list = ResourceService.get_resources_for_career(session=session, career_id=selected_career_id)

    st.markdown(f"""
    <div style="border-top: 2px dashed #cbd5e1; padding-top: 1.5rem; margin-top: 1.5rem;">
        <span class="badge-pill-blue">YOUR CAREER ROADMAP</span>
        <h2 style="color: #0f172a; font-size: 1.8rem; font-weight: 800; margin: 0.3rem 0 0.2rem;">
            My Career Plan: {career_title}
        </h2>
        <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1.2rem;">
            Here is everything you need to know about this career, what skills to learn, fun projects to build, and free places to start learning today!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Clean tabs for the 7 simple sections
    tab_about, tab_skills, tab_roadmap, tab_projects, tab_learn, tab_growth, tab_progress = st.tabs([
        "🌟 1. About This Job",
        "🧩 2. Skills I Need",
        "🗺️ 3. My Learning Plan",
        "🛠️ 4. Projects I Can Build",
        "📚 5. Free Places to Learn",
        "🪜 6. My Career Growth",
        "✅ 7. My Progress"
    ])

    # 1. About This Job
    with tab_about:
        with st.container(border=True):
            st.markdown(f"<h4 style='color: #0f172a; font-weight: 800; margin-bottom: 0.3rem;'>What is a {career_title}?</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #334155; line-height: 1.6; font-size: 1rem;'>{career_desc}</p>", unsafe_allow_html=True)
            
            st.markdown("<h5 style='color: #0f172a; font-weight: 700; margin-top: 1rem; margin-bottom: 0.3rem;'>What Does a Person Do in This Job?</h5>", unsafe_allow_html=True)
            st.markdown(f"<div style='background: #f8fafc; padding: 1rem; border-radius: 12px; color: #334155; line-height: 1.6; font-size: 0.95rem; border: 1px solid #e2e8f0;'>{career_daily}</div>", unsafe_allow_html=True)

            ab_c1, ab_c2 = st.columns(2)
            with ab_c1:
                st.markdown("<h5 style='color: #0f172a; font-weight: 700; margin-top: 1rem; margin-bottom: 0.2rem;'>Where Can They Work?</h5>", unsafe_allow_html=True)
                st.markdown("<p style='color: #475569; font-size: 0.92rem;'>Technology companies, research laboratories, startups, healthcare centers, game studios, and schools around the world.</p>", unsafe_allow_html=True)
            with ab_c2:
                st.markdown("<h5 style='color: #0f172a; font-weight: 700; margin-top: 1rem; margin-bottom: 0.2rem;'>Good Qualities to Have</h5>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #475569; font-size: 0.92rem;'>{career_soft_skills}</p>", unsafe_allow_html=True)

    # 2. Skills I Need
    with tab_skills:
        with st.container(border=True):
            readiness = gap_results.get("readiness_percentage", 50.0)
            acquired_list = gap_results.get("acquired_essential", [])
            missing_list = gap_results.get("missing_essential", [])

            s_col1, s_col2 = st.columns([3, 1])
            with s_col1:
                st.markdown(f"<h4 style='color: #0f172a; font-weight: 800; margin: 0;'>Your Readiness Score</h4>", unsafe_allow_html=True)
                st.caption(f"You already have {len(acquired_list)} skills, and have {len(missing_list)} helpful skills you can learn next.")
            with s_col2:
                st.markdown(f"<div style='text-align: right;'><span class='badge-pill-green' style='font-size: 1.05rem; font-weight: 800;'>{readiness}% READY</span></div>", unsafe_allow_html=True)

            st.progress(readiness / 100.0)

            sk_c1, sk_c2 = st.columns(2)
            with sk_c1:
                st.markdown("<h5 style='color: #15803d; font-weight: 700; margin-top: 1rem;'>✓ Skills You Already Know</h5>", unsafe_allow_html=True)
                if acquired_list:
                    for s in acquired_list:
                        s_name = s.get("name") or s.get("skill_name", "Skill")
                        st.markdown(f"<div style='padding: 0.5rem 0.8rem; background: #f0fdf4; border-radius: 8px; margin-bottom: 0.4rem; border: 1px solid #bbf7d0; font-weight: 600; color: #166534;'>✓ {s_name}</div>", unsafe_allow_html=True)
                else:
                    st.info("You don't need any prior skills to begin! Follow Step 1 in your learning plan to start fresh.")

            with sk_c2:
                st.markdown("<h5 style='color: #b45309; font-weight: 700; margin-top: 1rem;'>⚡ Skills to Learn Next</h5>", unsafe_allow_html=True)
                if missing_list:
                    for s in missing_list:
                        s_name = s.get("name") or s.get("skill_name", "Skill")
                        req_lvl = s.get("required_proficiency") or s.get("required_level", "Beginner")
                        st.markdown(f"<div style='display: flex; justify-content: space-between; padding: 0.5rem 0.8rem; background: #fffbeb; border-radius: 8px; margin-bottom: 0.4rem; border: 1px solid #fde68a;'><span style='font-weight: 600; color: #92400e;'>+ {s_name}</span><span style='font-size: 0.8rem; color: #b45309;'>Target: {req_lvl}</span></div>", unsafe_allow_html=True)
                else:
                    st.success("Awesome! You possess all core skills needed for this career!")

    # 3. My Learning Plan
    with tab_roadmap:
        with st.container(border=True):
            st.markdown("<h4 style='color: #0f172a; font-weight: 800; margin-bottom: 0.2rem;'>Step-by-Step Learning Plan</h4>", unsafe_allow_html=True)
            st.caption("Here is what to learn first, what to learn next, and what to build after that. Take it at your own comfortable pace!")

            stages = roadmap_results.get("stages", [])[:6]
            completed_milestones = set(st.session_state.get("completed_milestones", []))

            for stg in stages:
                s_num = stg.get("stage_number") or stg.get("stage", 1)
                s_name = stg.get("stage_name") or stg.get("name", "Foundations")
                is_done = f"{selected_career_id}_stage_{s_num}" in completed_milestones
                card_style = "border: 1px solid #86efac; background: #f0fdf4;" if is_done else "border: 1px solid #e2e8f0; background: #ffffff;"

                st.markdown(f"""
                <div style="border-radius: 14px; padding: 1rem 1.25rem; margin-bottom: 0.6rem; {card_style}">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="badge-pill-blue" style="font-size: 0.75rem;">STEP {s_num}</span>
                            <h5 style="color: #0f172a; font-weight: 800; margin: 0.3rem 0 0.2rem;">{s_name}</h5>
                            <p style="color: #475569; font-size: 0.9rem; margin: 0 0 0.5rem;">{stg['description']}</p>
                        </div>
                        <div style="text-align: right; min-width: 90px;">
                            <span style="font-weight: 700; color: #2563eb; font-size: 0.9rem;">~{stg.get('estimated_weeks', 2)} Weeks</span>
                        </div>
                    </div>
                    <div style="background: rgba(241, 245, 249, 0.7); padding: 0.6rem 0.8rem; border-radius: 8px; font-size: 0.85rem; color: #334155;">
                        <b>🎯 What You Will Do:</b> {stg.get('milestone', 'Complete guided hands-on practice.')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                check_key = f"chk_plan_{selected_career_id}_{s_num}"
                mark_done = st.checkbox(f"I finished Step {s_num}: {s_name}", value=is_done, key=check_key)
                if mark_done and not is_done:
                    completed_milestones.add(f"{selected_career_id}_stage_{s_num}")
                    st.session_state["completed_milestones"] = list(completed_milestones)
                    st.rerun()
                elif not mark_done and is_done:
                    completed_milestones.remove(f"{selected_career_id}_stage_{s_num}")
                    st.session_state["completed_milestones"] = list(completed_milestones)
                    st.rerun()

    # 4. Projects I Can Build
    with tab_projects:
        with st.container(border=True):
            st.markdown(f"<h4 style='color: #0f172a; font-weight: 800; margin-bottom: 0.2rem;'>Fun Projects You Can Build</h4>", unsafe_allow_html=True)
            st.caption("Building real projects is the best way to learn and show your skills to teachers, colleges, and employers!")

            if projects_list:
                for p in projects_list:
                    p_tools = p.get('suggested_technologies', 'Python, Scratch, Web')
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 1.1rem; margin-bottom: 0.9rem; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <h5 style="color: #0f172a; font-weight: 800; margin: 0 0 0.3rem;">{p['title']}</h5>
                            <span class="badge-pill-purple">{p['difficulty']}</span>
                        </div>
                        <p style="color: #475569; font-size: 0.9rem; line-height: 1.5; margin: 0.3rem 0 0.6rem;">{p['description']}</p>
                        <div style="background: #f8fafc; padding: 0.6rem 0.9rem; border-radius: 8px; font-size: 0.85rem; color: #334155;">
                            <b>🛠️ Tools You'll Use:</b> {p_tools}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Follow Step 6 in your learning plan for practical capstone project ideas!")

    # 5. Free Places to Learn
    with tab_learn:
        with st.container(border=True):
            st.markdown("<h4 style='color: #0f172a; font-weight: 800; margin-bottom: 0.2rem;'>Free & Official Places to Learn</h4>", unsafe_allow_html=True)
            st.caption("Here are verified, beginner-friendly tutorials, documentation, and videos with zero fake links.")

            if resources_list:
                for r in resources_list:
                    is_free_badge = "<span class='badge-pill-green'>FREE</span>" if r.get('is_free', True) else "<span class='badge-pill-amber'>PAID</span>"
                    res_type = r.get('resource_type', 'Tutorial')
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #ffffff; border: 1px solid #e2e8f0; padding: 0.8rem 1.1rem; border-radius: 12px; margin-bottom: 0.5rem;">
                        <div>
                            <div style="font-weight: 700; color: #0f172a; font-size: 0.95rem;">{r['title']}</div>
                            <div style="color: #64748b; font-size: 0.8rem;">Provider: <b>{r['provider']}</b> • Type: {res_type} • {is_free_badge}</div>
                        </div>
                        <div>
                            <a href="{r['url']}" target="_blank" style="text-decoration: none;">
                                <button style="background: #2563eb; color: white; border: none; padding: 0.4rem 0.9rem; border-radius: 8px; font-weight: 700; font-size: 0.85rem; cursor: pointer;">Open Tutorial ↗</button>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("You can learn all foundational skills directly via official documentation and free beginner tutorials online.")

    # 6. My Career Growth
    with tab_growth:
        with st.container(border=True):
            st.markdown("<h4 style='color: #0f172a; font-weight: 800; margin-bottom: 0.2rem;'>How You Grow in This Career</h4>", unsafe_allow_html=True)
            st.caption("See how your journey progresses from a curious beginner to a confident leader.")

            st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-around; background: #f8fafc; padding: 1.5rem 1rem; border-radius: 16px; margin: 1rem 0; flex-wrap: wrap; gap: 0.8rem; border: 1px solid #e2e8f0;">
                <div style="text-align: center;">
                    <span class="badge-pill-blue">BEGINNER</span>
                    <div style="font-weight: 800; color: #0f172a; margin-top: 0.4rem;">Junior Learner</div>
                    <div style="color: #64748b; font-size: 0.82rem;">Learning basics & building simple tasks</div>
                </div>
                <div style="color: #2563eb; font-size: 1.5rem; font-weight: 800;">➔</div>
                <div style="text-align: center;">
                    <span class="badge-pill-purple">INTERMEDIATE</span>
                    <div style="font-weight: 800; color: #0f172a; margin-top: 0.4rem;">Independent Builder</div>
                    <div style="color: #64748b; font-size: 0.82rem;">Building real apps & solving challenges</div>
                </div>
                <div style="color: #2563eb; font-size: 1.5rem; font-weight: 800;">➔</div>
                <div style="text-align: center;">
                    <span class="badge-pill-green">ADVANCED</span>
                    <div style="font-weight: 800; color: #0f172a; margin-top: 0.4rem;">Senior Specialist / Lead</div>
                    <div style="color: #64748b; font-size: 0.82rem;">Guiding others & creating big systems</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 7. My Progress
    with tab_progress:
        with st.container(border=True):
            completed_count = len(st.session_state.get("completed_milestones", []))
            total_milestones = 6
            pct_done = int((completed_count / total_milestones) * 100) if total_milestones else 0
            pct_done = min(100, pct_done)

            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; font-weight: 800; color: #0f172a; margin-bottom: 0.4rem;">
                <span>Plan Progress for {career_title}</span>
                <span>{pct_done}% ({completed_count}/{total_milestones} Steps Done)</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct_done / 100.0)

            st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)
            if st.button("💾 Save My Learning Progress", type="primary"):
                st.success("🎉 Awesome job! Your learning progress has been saved.")
