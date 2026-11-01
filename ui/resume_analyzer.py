# ui/resume_analyzer.py
"""
AI Resume Analyzer & Alignment View.
Upload PDF or DOCX resume files, extract technical skills against the 1,511 catalog,
compute match rates for target careers, and receive actionable ATS improvement advice.
Designed with the clean CoachPro light aesthetic.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import Career
from services.resume_service import ResumeService

def render_resume_analyzer():
    st.markdown("""
    <div style="margin-bottom: 1.2rem;">
        <h2 style="color: #0f2926; font-weight: 800; font-size: 1.6rem; margin-bottom: 0.2rem;">
            📄 AI Resume Analyzer & ATS Alignment
        </h2>
        <p style="color: #475569; font-size: 0.95rem; margin-bottom: 0;">
            Upload your resume (PDF or DOCX) to extract technical competencies, calculate alignment against target roles, and optimize for recruiter ATS systems.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        all_careers = session.query(Career).order_by(Career.title).all()
        career_titles = [c.title for c in all_careers]
        career_map = {c.title: c.career_id for c in all_careers}

        # Target Career Selection
        target_id = st.session_state.get("selected_career_id")
        def_idx = 0
        if target_id:
            for idx, c in enumerate(all_careers):
                if c.career_id == target_id:
                    def_idx = idx
                    break

        col_t, col_blank = st.columns([2, 1])
        with col_t:
            selected_target_title = st.selectbox(
                "Select Target Career to Align Resume Against:",
                career_titles,
                index=def_idx
            )
        target_career_id = career_map[selected_target_title]

        # Upload or Paste Tabs
        tab_upload, tab_paste = st.tabs(["📤 Upload PDF / DOCX Resume", "📝 Paste Resume Text"])

        resume_text = ""
        uploaded_file_name = "resume_input.txt"

        with tab_upload:
            uploaded_file = st.file_uploader(
                "Upload your resume file (PDF, DOCX, or TXT):",
                type=["pdf", "docx", "doc", "txt"]
            )
            if uploaded_file is not None:
                bytes_data = uploaded_file.read()
                uploaded_file_name = uploaded_file.name
                resume_text = ResumeService.extract_text(bytes_data, uploaded_file_name)
                st.success(f"✓ Successfully extracted text from `{uploaded_file_name}` ({len(resume_text.split())} words)")

        with tab_paste:
            pasted_text = st.text_area(
                "Or paste your plain text resume here:",
                height=180,
                placeholder="Paste your education, skills, work experience, and project descriptions here..."
            )
            if pasted_text.strip():
                resume_text = pasted_text.strip()
                uploaded_file_name = "pasted_resume.txt"

        if not resume_text:
            st.info("💡 Upload your resume or paste its text above to calculate your ATS match score.")
            return

        # Run Analysis
        analysis = ResumeService.analyze_resume(
            session=session,
            raw_text=resume_text,
            target_career_id=target_career_id,
            file_name=uploaded_file_name
        )

        st.markdown("<hr style='border: none; border-top: 1px solid #e2ece7; margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # Overview Metrics (CoachPro Stat Cards)
        match_rate = analysis["match_rate"]
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-icon-circle-teal">🎯</div>
                <div>
                    <div class="stat-value">{match_rate}%</div>
                    <div class="stat-label">Resume Match Rate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-icon-circle-purple">⚡</div>
                <div>
                    <div class="stat-value">{analysis['extracted_skills_count']}</div>
                    <div class="stat-label">Skills Extracted</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-icon-circle-amber">✓</div>
                <div>
                    <div class="stat-value">{len(analysis['matched_essential_skills'])}</div>
                    <div class="stat-label">Essential Matched</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-icon-circle-pink">!</div>
                <div>
                    <div class="stat-value">{len(analysis['missing_essential_skills'])}</div>
                    <div class="stat-label">Missing for ATS</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Actionable Suggestions Card
        if analysis["suggestions"]:
            st.markdown("<h4 style='color: #0f2926; font-weight: 800; margin-bottom: 0.5rem;'>💡 ATS & Content Optimization Suggestions</h4>", unsafe_allow_html=True)
            for sugg in analysis["suggestions"]:
                st.markdown(f"""
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 0.75rem 1rem; border-radius: 10px; margin-bottom: 0.5rem; color: #166534; font-size: 0.9rem;">
                    {sugg}
                </div>
                """, unsafe_allow_html=True)

        # Two columns for skills breakdown
        c_left, c_right = st.columns(2)

        with c_left:
            st.markdown("<h5 style='color: #0f2926; font-weight: 800; margin-top: 1rem;'>🔍 Identified Technical Skills in Resume:</h5>", unsafe_allow_html=True)
            if analysis["extracted_skills"]:
                badges_html = " ".join([
                    f"<span class='skill-pill-matched'>{s['name']}</span>"
                    for s in analysis["extracted_skills"]
                ])
                st.markdown(f"<div style='margin-bottom: 1rem;'>{badges_html}</div>", unsafe_allow_html=True)

                if st.button("➕ Import Extracted Skills into My Active Profile", type="primary"):
                    student_skills = st.session_state.get("student_skills", {})
                    for sk in analysis["extracted_skills"]:
                        s_name = sk["name"]
                        if s_name not in student_skills:
                            student_skills[s_name] = "Intermediate"
                    st.session_state["student_skills"] = student_skills
                    st.success(f"Added {len(analysis['extracted_skills'])} skills to your active profile!")
                    st.rerun()
            else:
                st.warning("No explicit technical skills matching our database were detected.")

        with c_right:
            st.markdown(f"<h5 style='color: #0f2926; font-weight: 800; margin-top: 1rem;'>🎯 Match for {analysis['target_career_title']}:</h5>", unsafe_allow_html=True)
            if analysis["matched_essential_skills"]:
                st.markdown("<div style='color: #047857; font-weight: 700; margin-bottom: 0.3rem;'>✓ Matched Essential Skills:</div>", unsafe_allow_html=True)
                for ms in analysis["matched_essential_skills"]:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.7rem; background: #f0fdf4; border-radius: 8px; margin-bottom: 0.3rem; border: 1px solid #dcfce7;">
                        <span style="font-weight: 700; color: #15803d;">{ms['name']}</span>
                        <span style="color: #166534; font-size: 0.8rem;">Found in resume</span>
                    </div>
                    """, unsafe_allow_html=True)

            if analysis["missing_essential_skills"]:
                st.markdown("<div style='color: #b45309; font-weight: 700; margin: 0.8rem 0 0.3rem;'>✗ Missing Essential Skills (Recommended for ATS):</div>", unsafe_allow_html=True)
                for mis in analysis["missing_essential_skills"]:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.7rem; background: #fffbeb; border-radius: 8px; margin-bottom: 0.3rem; border: 1px solid #fef3c7;">
                        <span style="font-weight: 700; color: #92400e;">{mis['name']}</span>
                        <span style="color: #b45309; font-size: 0.8rem;">Target: {mis['required_proficiency']}</span>
                    </div>
                    """, unsafe_allow_html=True)

        with st.expander("📄 View Extracted Text Preview"):
            st.text(analysis["raw_text_preview"])
