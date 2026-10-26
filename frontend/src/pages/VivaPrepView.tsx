import React, { useState } from 'react';
import {
  GraduationCap,
  BookOpen,
  CheckCircle2,
  Cpu,
  Database,
  Layers,
  Code2,
  FileText,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

export const VivaPrepView: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const vivaQuestions = [
    {
      q: '1. What is an Agentic Workflow and how does it differ from ordinary ChatGPT prompts?',
      a: (
        <div className="space-y-2">
          <p>
            An <strong>Agentic Workflow</strong> is a multi-step orchestrated pipeline where specialized software components coordinate to accomplish a complex goal.
          </p>
          <ul className="list-disc list-inside space-y-1 text-slate-300">
            <li>
              <strong>Ordinary Prompt:</strong> Involves sending a single prompt to an LLM, hoping it won't hallucinate skills, timelines, or invalid steps.
            </li>
            <li>
              <strong>Our Agentic System:</strong> Decomposes career planning into 6 distinct stages:
              (1) Profile Analysis $\rightarrow$ (2) Deterministic Recommendation Engine $\rightarrow$ (3) Skill-Gap Analysis $\rightarrow$ (4) Roadmap Generation $\rightarrow$ (5) Quality Guardrails Review $\rightarrow$ (6) Human-in-the-Loop Approval.
            </li>
          </ul>
        </div>
      )
    },
    {
      q: '2. How does the Career Recommendation Engine calculate match scores?',
      a: (
        <div className="space-y-2">
          <p>
            We use a <strong>transparent multi-factor weighted scoring formula</strong> instead of arbitrary random numbers:
          </p>
          <div className="p-3 rounded-xl bg-[#0B0B0E] font-mono text-[11px] text-[#E0AAFF]">
            Total Score = (0.40 × Skill_Score) + (0.30 × Interest_Score) + (0.15 × Field_Pref) + (0.10 × Experience) + (0.05 × Goals)
          </div>
          <p className="text-slate-300">
            - Technical skills are weighted highest (40%), comparing required and recommended skills.
            - Overlap ratios are bounded between 15% and 98.5% and labeled as educational compatibility, never as employment guarantees.
          </p>
        </div>
      )
    },
    {
      q: '3. Why is a deterministic rule-based fallback critical for an AI project?',
      a: (
        <p className="text-slate-300">
          In high-stakes educational or academic evaluations, relying solely on an external paid API is risky due to rate limits, internet drops, or quota exhaustion. Our system integrates Google Gemini for conversational assistance, but features a <strong>100% deterministic offline fallback</strong> built upon our institutional career knowledge base, ensuring zero downtime during college viva demonstrations.
        </p>
      )
    },
    {
      q: '4. Why did you choose FastAPI, Pydantic, and SQLAlchemy for the backend?',
      a: (
        <ul className="list-disc list-inside space-y-1 text-slate-300">
          <li><strong>FastAPI:</strong> Modern high-performance asynchronous Python framework with auto-generated OpenAPI/Swagger documentation at <code>/docs</code>.</li>
          <li><strong>Pydantic:</strong> Strict data validation at runtime, rejecting malformed requests (HTTP 422) before touching the database.</li>
          <li><strong>SQLAlchemy:</strong> Industry-standard ORM providing decoupled database queries and seamless migration support from SQLite to PostgreSQL.</li>
        </ul>
      )
    },
    {
      q: '5. How does the Skill-Gap Analysis categorize student competencies?',
      a: (
        <p className="text-slate-300">
          It classifies required role skills into three transparent categories:
          <br /><strong>1. Confirmed:</strong> Declared directly in the student's academic profile.
          <br /><strong>2. Partially Developed:</strong> Foundation reported (e.g. general Python declared, but advanced PyTorch omitted).
          <br /><strong>3. Not Yet Reported:</strong> No matching foundational indicator found in profile.
          <br /><em>Note:</em> The system emphasizes that self-reported data is not independently certified.
        </p>
      )
    }
  ];

  const presentationSlides = [
    { slide: 'Slide 1', title: 'Title & Team', content: 'Intelligent Career Path Planning Agent | BE AI & Data Science Mini-Project' },
    { slide: 'Slide 2', title: 'Problem Statement', content: 'Uncertainty in engineering career trajectories, lack of roadmap clarity, unverified online advice.' },
    { slide: 'Slide 3', title: 'Proposed System', content: 'Explainable AI guidance platform combining deterministic mathematical scoring with agentic LLM assistance.' },
    { slide: 'Slide 4', title: 'System Architecture', content: 'Three-tier architecture: React + TypeScript UI, FastAPI REST gateway, PostgreSQL/SQLAlchemy, and Agent Orchestrator.' },
    { slide: 'Slide 5', title: 'Recommendation Algorithm', content: 'Multi-factor weighted scoring methodology with explicit formula breakdown.' },
    { slide: 'Slide 6', title: 'Skill-Gap Analysis', content: 'Categorization matrix: Confirmed, Partially Developed, and Unreported skills with priority ordering.' },
    { slide: 'Slide 7', title: 'Personalized Roadmap', content: '5-phase curriculum (Foundations $\rightarrow$ Core $\rightarrow$ Practice $\rightarrow$ Projects $\rightarrow$ Viva) respecting weekly hours.' },
    { slide: 'Slide 8', title: 'Agentic Workflow & Human Review', content: '6-component pipeline with quality review guardrails and human-in-the-loop approval.' },
    { slide: 'Slide 9', title: 'Testing & Verification', content: 'Pytest automated test suite with 11 real test cases covering validation, scoring, fallback, and API responses.' },
    { slide: 'Slide 10', title: 'Conclusion & Future Work', content: 'Summary of achievements, RAG integration for college syllabus notes, and deployment readiness.' }
  ];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 sm:p-8 bg-[#14141D] border border-white/5 rounded-3xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-[#C77DFF]" />
            <h2 className="text-xl font-bold text-white">Project Viva Defense & Academic Hub</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Complete preparation guide for your BE Artificial Intelligence & Data Science mini-project presentation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs px-3 py-1 rounded-full bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 font-semibold">
            11/11 Automated Tests Passing
          </span>
        </div>
      </div>

      {/* Viva Questions Accordion */}
      <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6 sm:p-8">
        <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-[#C77DFF]" />
          <span>Top 5 Viva Questions & Explanations</span>
        </h3>

        <div className="space-y-3">
          {vivaQuestions.map((item, idx) => (
            <div
              key={idx}
              className="bg-[#0B0B0E] border border-white/5 rounded-2xl overflow-hidden transition-all"
            >
              <button
                onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
                className="w-full p-4 text-left flex items-center justify-between text-xs font-bold text-white hover:text-[#C77DFF]"
              >
                <span>{item.q}</span>
                {openIndex === idx ? (
                  <ChevronUp className="w-4 h-4 text-slate-400 shrink-0 ml-2" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-slate-400 shrink-0 ml-2" />
                )}
              </button>
              {openIndex === idx && (
                <div className="px-4 pb-4 pt-1 text-xs text-slate-300 border-t border-white/5">
                  {item.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 10-Slide Presentation Outline */}
      <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6 sm:p-8">
        <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
          <FileText className="w-4 h-4 text-[#C77DFF]" />
          <span>10-Slide Presentation Outline for College Review</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {presentationSlides.map((s, idx) => (
            <div key={idx} className="bg-[#0B0B0E] border border-white/5 rounded-2xl p-4">
              <span className="text-[10px] font-bold text-[#E0AAFF] uppercase tracking-wider">
                {s.slide}
              </span>
              <h4 className="text-xs font-bold text-white mt-1">{s.title}</h4>
              <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">{s.content}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
