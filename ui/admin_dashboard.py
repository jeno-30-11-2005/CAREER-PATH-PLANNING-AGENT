# ui/admin_dashboard.py
"""
Admin Management Dashboard View.
Provides database administration, system statistics, and bulk CSV/JSON ingestion
with automated duplicate detection, schema validation, and audit logging.
Styled with the clean CoachPro light aesthetic.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import DataImportLog, TechnicalSkill, Career, Project
from services.admin_service import AdminService

def render_admin_dashboard():
    st.markdown("""
    <div style="margin-bottom: 1.2rem;">
        <h2 style="color: #0f2926; font-weight: 800; font-size: 1.6rem; margin-bottom: 0.2rem;">
            ⚙️ Administrator Management Portal
        </h2>
        <p style="color: #475569; font-size: 0.95rem; margin-bottom: 0;">
            System administration, catalog governance, bulk CSV/JSON ingestion, and automated data import audit logs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        # Check authentication state
        is_authenticated = st.session_state.get("admin_authenticated", False)

        if not is_authenticated:
            st.markdown("""
            <div class="card-coachpro" style="max-width: 480px; margin: 1.5rem auto; text-align: center;">
                <h3 style="color: #0f2926; margin-top: 0; font-size: 1.3rem; font-weight: 800;">🔐 Administrator Sign-In</h3>
                <p style="color: #64748b; font-size: 0.9rem;">Sign in with your administrative credentials to manage database records and bulk imports.</p>
            </div>
            """, unsafe_allow_html=True)

            login_col1, login_col2, login_col3 = st.columns([1, 1.8, 1])
            with login_col2:
                username = st.text_input("Username:", value="admin")
                password = st.text_input("Password:", type="password", value="admin123")
                
                if st.button("Sign In to Admin Portal", type="primary", use_container_width=True):
                    admin = AdminService.authenticate(session, username, password)
                    if admin:
                        st.session_state["admin_authenticated"] = True
                        st.session_state["admin_user"] = admin.username
                        st.success("✓ Access granted! Loading dashboard...")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
            return

        # Authenticated Admin View
        col_hdr1, col_hdr2 = st.columns([3, 1])
        with col_hdr1:
            st.markdown(f"<strong style='color: #0f2926;'>Logged in as:</strong> <span class='badge-pill-mint'>SuperAdmin ({st.session_state.get('admin_user', 'admin')})</span>", unsafe_allow_html=True)
        with col_hdr2:
            if st.button("Sign Out", use_container_width=True):
                st.session_state["admin_authenticated"] = False
                st.rerun()

        # 1. System Overview Metrics
        stats = AdminService.get_system_stats(session)

        st.markdown("<h3 style='color: #0f2926; font-weight: 800; margin: 1rem 0 0.5rem;'>📊 System & Database Health</h3>", unsafe_allow_html=True)
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("Technical Skills", f"{stats['total_skills']:,}", f"{stats['active_skills']} Active")
        with m2:
            st.metric("Careers", f"{stats['total_careers']:,}", f"{stats['career_categories']} Families")
        with m3:
            st.metric("Portfolio Projects", f"{stats['total_projects']:,}", "Active")
        with m4:
            st.metric("Resources", f"{stats['total_resources']:,}", "Verified")
        with m5:
            st.metric("Registered Students", f"{stats['total_students']:,}", f"{stats['import_logs']} Ingestion Logs")

        st.markdown("<hr style='border: none; border-top: 1px solid #e2ece7; margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 2. Main Admin Tabs
        t_import, t_logs, t_browse = st.tabs(["📥 Bulk Data Ingestion", "📜 Import Audit Logs", "🔍 Database Record Explorer"])

        with t_import:
            st.markdown("<h4 style='color: #0f2926; font-weight: 800;'>Bulk Import Technical Skills</h4>", unsafe_allow_html=True)
            st.markdown("<p style='color: #475569;'>Upload CSV or paste JSON data to ingest new skills with automated schema validation and duplicate checking.</p>", unsafe_allow_html=True)

            imp_type = st.radio("Select Ingestion Format:", ["CSV Upload", "JSON Paste"], horizontal=True)

            if imp_type == "CSV Upload":
                st.markdown("""
                **CSV Requirements:** Columns `name`, `category`, `subcategory`, `description`, `difficulty_level`, `learning_priority`
                """)
                csv_sample = "name,category,subcategory,description,difficulty_level,learning_priority\nMojo,Programming Languages,AI Programming,Fast Python-compatible language for AI hardware,Advanced,High\nLangfuse,DevOps,LLM Observability,Open-source LLM engineering and observability platform,Intermediate,High"
                st.download_button("Download CSV Template", csv_sample, file_name="skills_import_template.csv", mime="text/csv")

                uploaded_csv = st.file_uploader("Upload CSV file:", type=["csv"])
                if uploaded_csv is not None:
                    csv_text = uploaded_csv.read().decode("utf-8")
                    if st.button("Validate & Ingest CSV", type="primary"):
                        res = AdminService.import_skills_from_csv(session, csv_text, imported_by=st.session_state.get("admin_user", "admin"))
                        st.success(f"✓ Ingestion Complete: {res['inserted_records']} records added, {res['rejected_records']} duplicates/rejected out of {res['total_records']} total.")
                        if res["errors"]:
                            with st.expander("View Ingestion Notices / Rejected Rows"):
                                for err in res["errors"][:15]:
                                    st.caption(err)
            else:
                json_sample = '[\n  {\n    "name": "Mojo Programming Language",\n    "category": "Programming Languages",\n    "subcategory": "AI Compilers",\n    "description": "High performance language for AI hardware accelerators.",\n    "difficulty_level": "Advanced",\n    "learning_priority": "High"\n  }\n]'
                pasted_json = st.text_area("Paste JSON Array:", value=json_sample, height=180)
                if st.button("Validate & Ingest JSON", type="primary"):
                    res = AdminService.import_skills_from_json(session, pasted_json, imported_by=st.session_state.get("admin_user", "admin"))
                    if "error" in res:
                        st.error(res["error"])
                    else:
                        st.success(f"✓ Ingestion Complete: {res['inserted_records']} added, {res['rejected_records']} rejected out of {res['total_records']}.")
                        if res["errors"]:
                            with st.expander("View Ingestion Notices"):
                                for err in res["errors"]:
                                    st.caption(err)

        with t_logs:
            st.markdown("<h4 style='color: #0f2926; font-weight: 800;'>System Ingestion Audit History</h4>", unsafe_allow_html=True)
            logs = session.query(DataImportLog).order_by(DataImportLog.timestamp.desc()).limit(20).all()

            if logs:
                for l in logs:
                    st.markdown(f"""
                    <div style="background: #ffffff; padding: 0.9rem 1.2rem; border-radius: 12px; margin-bottom: 0.6rem; border: 1px solid #e2ece7; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
                        <div style="display: flex; justify-content: space-between;">
                            <strong style="color: #0f2926;">{l.entity_type} ({l.source_format})</strong>
                            <span style="color: #64748b; font-size: 0.85rem;">{l.timestamp.strftime('%Y-%m-%d %H:%M:%S')} by <em>{l.imported_by}</em></span>
                        </div>
                        <div style="color: #334155; font-size: 0.85rem; margin-top: 0.3rem;">
                            Total: <strong>{l.total_records}</strong> | Inserted: <span style="color: #047857; font-weight: 700;">{l.inserted_records}</span> | Rejected: <span style="color: #b45309; font-weight: 700;">{l.rejected_records}</span>
                        </div>
                        {f'<div style="color: #b45309; font-size: 0.8rem; margin-top: 0.3rem; white-space: pre-line;">{l.error_log[:200]}</div>' if l.error_log else ''}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No bulk import logs recorded yet.")

        with t_browse:
            st.markdown("<h4 style='color: #0f2926; font-weight: 800;'>Database Catalog Inspector</h4>", unsafe_allow_html=True)
            ent_choice = st.selectbox("Inspect Table:", ["Technical Skills (1,511)", "Careers (505)", "Portfolio Projects (505)"])

            if "Skills" in ent_choice:
                sample_skills = session.query(TechnicalSkill).limit(30).all()
                data = [{"ID": s.skill_id, "Name": s.name, "Category": s.category.name if s.category else "", "Difficulty": s.difficulty_level, "Active": s.is_active} for s in sample_skills]
                st.dataframe(data, use_container_width=True)
            elif "Careers" in ent_choice:
                sample_careers = session.query(Career).limit(30).all()
                data = [{"ID": c.career_id, "Title": c.title, "Family": c.category.name if c.category else "", "Difficulty": c.difficulty_level, "Suitability": c.entry_level_suitability} for c in sample_careers]
                st.dataframe(data, use_container_width=True)
            else:
                sample_projects = session.query(Project).limit(30).all()
                data = [{"ID": p.project_id, "Title": p.title, "Category": p.category, "Difficulty": p.difficulty, "Est. Hours": p.estimated_hours} for p in sample_projects]
                st.dataframe(data, use_container_width=True)
