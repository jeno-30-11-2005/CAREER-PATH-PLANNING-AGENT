# ui/interests_catalog.py
"""
Areas of Interest Catalog View.
Interactive browser across 250+ interest areas and 27 domains.
Allows students to explore interests and tag them to their career profile.
"""
import streamlit as st
from database.connection import get_db_session
from database.models import AreaOfInterest, InterestCategory

def render_interests_catalog():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.3rem;">🎯 Areas of Interest Catalog</h2>
        <p style="color: #94a3b8; font-size: 1rem;">
            Discover 250+ distinct fields of interest across 27 specialized engineering and research domains.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as session:
        f_c1, f_c2 = st.columns([2, 1.5])
        with f_c1:
            search_query = st.text_input("🔍 Search interest topics:", placeholder="e.g. Robotics, Blockchain, Autonomous Driving, NLP...")
        with f_c2:
            all_cats = [c.name for c in session.query(InterestCategory.name).order_by(InterestCategory.name).all()]
            selected_cat = st.selectbox("Filter Category:", ["All Categories"] + all_cats)

        query = session.query(AreaOfInterest).join(InterestCategory)
        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(
                (AreaOfInterest.name.ilike(term)) |
                (AreaOfInterest.description.ilike(term)) |
                (AreaOfInterest.industry_domain.ilike(term))
            )
        if selected_cat != "All Categories":
            query = query.filter(InterestCategory.name == selected_cat)

        total_interests = query.count()
        st.markdown(f"<div style='color: #a5b4fc; margin-bottom: 1rem;'>Showing <strong>{min(total_interests, 60)}</strong> of <strong>{total_interests}</strong> interest areas:</div>", unsafe_allow_html=True)

        interests = query.limit(60).all()
        student_interests = set(st.session_state.get("student_interests", []))

        # Render in a clean 3-column grid
        cols = st.columns(3)
        for idx, item in enumerate(interests):
            col = cols[idx % 3]
            is_selected = item.interest_id in student_interests or item.name in student_interests

            with col:
                st.markdown(f"""
                <div style="background: rgba(30, 27, 75, 0.4); border: 1px solid {'#10b981' if is_selected else 'rgba(139, 92, 246, 0.2)'}; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; min-height: 150px;">
                    <div style="font-weight: 700; color: #f1f5f9; font-size: 1rem; margin-bottom: 0.3rem;">{item.name}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 0.5rem;">{item.category.name} | {item.industry_domain or 'Tech'}</div>
                    <div style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.4; margin-bottom: 0.6rem;">{item.description[:110]}...</div>
                </div>
                """, unsafe_allow_html=True)

                if is_selected:
                    if st.button(f"✓ Selected (Remove)", key=f"intr_rem_{item.interest_id}", use_container_width=True):
                        if item.interest_id in student_interests:
                            student_interests.remove(item.interest_id)
                        if item.name in student_interests:
                            student_interests.remove(item.name)
                        st.session_state["student_interests"] = list(student_interests)
                        st.rerun()
                else:
                    if st.button(f"➕ Add to My Interests", key=f"intr_add_{item.interest_id}", use_container_width=True):
                        student_interests.add(item.interest_id)
                        st.session_state["student_interests"] = list(student_interests)
                        st.rerun()
