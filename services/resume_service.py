# services/resume_service.py
"""
Resume Parser & Career Alignment Analyzer.
Extracts text from PDF (PyMuPDF) and DOCX (python-docx) files,
matches competencies against 1,511 technical skills and aliases,
computes match percentage against target careers, and generates ATS optimization advice.
"""
import io
import re
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from database.models import (
    TechnicalSkill, Career, ResumeAnalysis
)

class ResumeService:
    @staticmethod
    def extract_text(file_bytes: bytes, file_name: str) -> str:
        """
        Extracts raw text from PDF, DOCX, or text files.
        """
        text = ""
        ext = file_name.lower().split(".")[-1]

        if ext == "pdf":
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                for page in doc:
                    text += page.get_text() + "\n"
            except Exception as e:
                text = f"[PDF Extraction Error: {str(e)}]"

        elif ext in ["docx", "doc"]:
            try:
                import docx
                doc = docx.Document(io.BytesIO(file_bytes))
                for para in doc.paragraphs:
                    text += para.text + "\n"
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            text += cell.text + " "
                        text += "\n"
            except Exception as e:
                text = f"[DOCX Extraction Error: {str(e)}]"
        else:
            try:
                text = file_bytes.decode("utf-8", errors="ignore")
            except Exception:
                text = str(file_bytes)

        return text.strip()

    @staticmethod
    def analyze_resume(
        session: Session,
        raw_text: str,
        target_career_id: Optional[int] = None,
        file_name: str = "resume.txt",
        student_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Analyzes resume text against the 1,511 technical skills and compares with target career.
        """
        if not raw_text:
            return {
                "error": "No text extracted from resume.",
                "extracted_skills": [],
                "match_rate": 0
            }

        # Pre-cache technical skills and aliases
        all_skills = session.query(TechnicalSkill).all()
        from database.models import SkillAlias
        all_aliases = session.query(SkillAlias).all()
        alias_map = {}
        for a in all_aliases:
            if a.skill_id not in alias_map:
                alias_map[a.skill_id] = []
            alias_map[a.skill_id].append(a.alias_name.lower())

        normalized_text = " " + re.sub(r'[^a-zA-Z0-9+#.\-]', ' ', raw_text.lower()) + " "

        extracted_skills: List[Dict[str, Any]] = []
        seen_skill_ids = set()

        STOP_WORDS = {"and", "the", "core", "tool", "tools", "framework", "system", "systems", "development", "data", "web"}

        # Match skills against text
        for skill in all_skills:
            sk_name_low = skill.name.lower()
            matched = False

            # 1. Exact full name match
            pattern = r'(?:\b|\s)' + re.escape(sk_name_low) + r'(?:\b|\s)'
            if re.search(pattern, normalized_text):
                matched = True

            # 2. Check aliases
            if not matched and skill.skill_id in alias_map:
                for alias in alias_map[skill.skill_id]:
                    if len(alias) >= 2 and re.search(r'(?:\b|\s)' + re.escape(alias) + r'(?:\b|\s)', normalized_text):
                        matched = True
                        break

            # 3. Check prominent headwords (e.g. "Docker" for "Docker Containerization", "PyTorch" for "PyTorch Framework")
            if not matched:
                words = re.findall(r'[a-zA-Z0-9+#.\-]+', sk_name_low)
                for w in words:
                    if len(w) >= 4 and w not in STOP_WORDS:
                        if re.search(r'(?:\b|\s)' + re.escape(w) + r'(?:\b|\s)', normalized_text):
                            matched = True
                            break

            if matched and skill.skill_id not in seen_skill_ids:
                seen_skill_ids.add(skill.skill_id)
                extracted_skills.append({
                    "skill_id": skill.skill_id,
                    "name": skill.name,
                    "category": skill.category.name if skill.category else "Technical",
                    "difficulty": skill.difficulty_level
                })

        # Target Career Match Analysis
        career_analysis = None
        target_career = None
        matched_essential = []
        missing_essential = []
        matched_preferred = []
        missing_preferred = []
        match_rate = 0.0

        if target_career_id:
            target_career = session.query(Career).filter_by(career_id=target_career_id).first()
            if target_career:
                extracted_ids = {s["skill_id"] for s in extracted_skills}

                for cs in target_career.skills:
                    sk = cs.skill
                    if not sk:
                        continue
                    item = {
                        "skill_id": cs.skill_id,
                        "name": sk.name,
                        "required_proficiency": cs.required_proficiency,
                        "importance_weight": cs.importance_weight
                    }
                    if cs.skill_type == "essential":
                        if cs.skill_id in extracted_ids:
                            matched_essential.append(item)
                        else:
                            missing_essential.append(item)
                    elif cs.skill_type == "preferred":
                        if cs.skill_id in extracted_ids:
                            matched_preferred.append(item)
                        else:
                            missing_preferred.append(item)

                total_ess = len(matched_essential) + len(missing_essential)
                total_pref = len(matched_preferred) + len(missing_preferred)

                ess_score = (len(matched_essential) / total_ess) if total_ess else 1.0
                pref_score = (len(matched_preferred) / total_pref) if total_pref else 1.0

                match_rate = round(((0.75 * ess_score) + (0.25 * pref_score)) * 100, 1)

        # Generate Actionable ATS & Content Improvement Recommendations
        suggestions = []
        if missing_essential:
            missing_names = [s["name"] for s in missing_essential[:4]]
            suggestions.append(
                f"High ATS Priority: Add missing essential keywords {', '.join(missing_names)} "
                f"in your project experience descriptions to improve automated recruiter screening scores."
            )
        if len(extracted_skills) < 5:
            suggestions.append(
                "Skill Visibility: Your resume mentions relatively few explicit technical frameworks. "
                "Add a dedicated 'Technical Skills' section categorizing languages, frameworks, developer tools, and databases."
            )
        if not re.search(r'\b(deployed|architected|optimized|engineered|reduced|increased|scaled|automated)\b', normalized_text):
            suggestions.append(
                "Action Verbs: Strengthen your bullet points with high-impact impact verbs like "
                "'Architected', 'Engineered', 'Optimized', and 'Automated' alongside measurable metrics (e.g. 'reduced latency by 35%')."
            )
        if target_career and match_rate < 50:
            suggestions.append(
                f"Portfolio Alignment: For {target_career.title}, highlight at least one capstone project "
                f"demonstrating end-to-end production deployment with containerization and automated testing."
            )

        # Word count & reading metrics
        words = raw_text.split()
        word_count = len(words)

        result = {
            "file_name": file_name,
            "word_count": word_count,
            "extracted_skills_count": len(extracted_skills),
            "extracted_skills": extracted_skills,
            "target_career_id": target_career_id,
            "target_career_title": target_career.title if target_career else None,
            "target_career_category": target_career.category.name if target_career else None,
            "match_rate": match_rate,
            "matched_essential_skills": matched_essential,
            "missing_essential_skills": missing_essential,
            "matched_preferred_skills": matched_preferred,
            "missing_preferred_skills": missing_preferred,
            "suggestions": suggestions,
            "raw_text_preview": raw_text[:400] + ("..." if len(raw_text) > 400 else "")
        }

        # Optional database persistence
        if student_id and target_career_id:
            analysis_rec = ResumeAnalysis(
                student_id=student_id,
                file_name=file_name,
                extracted_text=raw_text[:2000],
                extracted_skills=",".join([s["name"] for s in extracted_skills]),
                target_career_id=target_career_id,
                matched_skills=",".join([s["name"] for s in matched_essential + matched_preferred]),
                missing_skills=",".join([s["name"] for s in missing_essential + missing_preferred]),
                improvement_suggestions="\n".join(suggestions)
            )
            session.add(analysis_rec)
            session.commit()
            result["analysis_id"] = analysis_rec.analysis_id

        return result
