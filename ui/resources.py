# ui/resources.py
"""
Curated Learning Resources View.
Browse 500+ verified courses, official documentation, open access textbooks,
and interactive tutorials with live links and free/paid indicators.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import LearningResource
from services.resource_service import ResourceService

def render_resources():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">📚 Curated Learning Resources</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Access verified official documentation, open-source textbooks, and reputable courses without broken links or fabricated certificates.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        f_c1, f_c2, f_c3, f_c4 = st.columns([2, 1.2, 1, 1])

        with f_c1:
            search_query = st.text_input("🔍 Search resources by title or provider:", placeholder="e.g. PyTorch, PostgreSQL, Kubernetes, MDN...")

        with f_c2:
            all_types = [row[0] for row in session.query(LearningResource.resource_type).distinct().all() if row[0]]
            selected_type = st.selectbox("Resource Type:", ["All Types"] + all_types)

        with f_c3:
            selected_diff = st.selectbox("Difficulty:", ["All", "Beginner", "Intermediate", "Advanced"])

        with f_c4:
            free_only = st.checkbox("Free Only", value=True)

        type_arg = None if selected_type == "All Types" else selected_type
        diff_arg = None if selected_diff == "All" else selected_diff

        resources = ResourceService.get_all_resources(
            session=session,
            search_query=search_query,
            free_only=free_only,
            resource_type=type_arg,
            difficulty=diff_arg,
            limit=40
        )

        st.markdown(f"<div style='color: #a5b4fc; margin-bottom: 1rem;'>Showing <strong>{len(resources)}</strong> verified resources:</div>", unsafe_allow_html=True)

        # 2-column card layout
        cols = st.columns(2)
        for idx, res in enumerate(resources):
            col = cols[idx % 2]
            with col:
                free_badge = "🟢 FREE" if res["is_free"] else "🔵 PAID/BOOK"
                st.markdown(f"""
                <div style="background: rgba(30, 27, 75, 0.4); border: 1px solid rgba(139, 92, 246, 0.2); padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; min-height: 180px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.3rem;">
                        <span style="color: #a5b4fc; font-size: 0.8rem; font-weight: 600;">{res['provider']}</span>
                        <span style="background: {'rgba(16, 185, 129, 0.2)' if res['is_free'] else 'rgba(56, 189, 248, 0.2)'}; color: {'#10b981' if res['is_free'] else '#38bdf8'}; font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">
                            {free_badge}
                        </span>
                    </div>
                    <div style="font-weight: 700; color: #ffffff; font-size: 1.05rem; margin-bottom: 0.4rem;">{res['title']}</div>
                    <div style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.6rem;">
                        Type: <strong>{res['resource_type']}</strong> | Level: <strong>{res['difficulty']}</strong> | Lang: {res['language']}
                    </div>
                    <div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 0.8rem;">
                        Associated Career: {res['career_title']}
                    </div>
                    <div>
                        <a href="{res['url']}" target="_blank" style="display: inline-block; background: #4f46e5; color: #ffffff; text-decoration: none; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600;">
                            🔗 Open Resource ↗
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
