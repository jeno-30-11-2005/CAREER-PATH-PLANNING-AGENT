import React, { useState } from 'react';
import {
  TrendingUp,
  Sparkles,
  ArrowUpRight,
  ChevronDown,
  CheckCircle2,
  BookOpen,
  Target,
  Zap,
  Clock,
  Layers,
  FileSpreadsheet,
  Download,
  Award,
  BarChart2
} from 'lucide-react';
import { DashboardOverview, RecommendationItem, StudentProfile } from '../types';

interface DashboardViewProps {
  overview: DashboardOverview | null;
  student: StudentProfile | null;
  recommendations: RecommendationItem[];
  onExploreAI: () => void;
  onSelectRole: (slug: string) => void;
  onNavigateToRoadmap: () => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  overview,
  student,
  recommendations,
  onExploreAI,
  onSelectRole,
  onNavigateToRoadmap
}) => {
  const [timeFilter, setTimeFilter] = useState('1M');
  const [reportFilter, setReportFilter] = useState('Semester 6');

  const topMatch = recommendations[0];
  const readinessScore = topMatch ? topMatch.match_score : 84.5;
  const targetRoleTitle = overview?.active_roadmap?.target_role || (topMatch ? topMatch.career_role.title : 'AI Engineer');
  const progressPercent = overview?.overall_progress_percentage || 0;

  return (
    <div className="space-y-6">
      {/* SECTION 1: General Report (Rubick Top Section) */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700">
            General Career Readiness Report
          </h2>
          <div className="flex items-center gap-1.5 bg-white border border-slate-200 px-3 py-1 rounded-lg text-xs font-semibold text-slate-600 shadow-sm">
            <span>{reportFilter}</span>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-5">
          {/* Card 1: Main Metric Card (like Rubick $54.143 card) - 5 cols */}
          <div className="md:col-span-5 rubick-card p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-[#1b3bbb]">
                  <Award className="w-5 h-5" />
                </div>
                <span className="text-xs font-semibold text-slate-400">Target Compatibility</span>
              </div>
              <div className="my-4">
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-slate-900 tracking-tight">
                    {readinessScore}%
                  </span>
                  <span className="text-xs font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full flex items-center">
                    +14.2% <ArrowUpRight className="w-3 h-3" />
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  Overall match for <span className="font-semibold text-slate-800">{targetRoleTitle}</span> based on 5-factor weighted algorithm.
                </p>
              </div>
            </div>

            {/* Sub-breakdown rows */}
            <div className="pt-3 border-t border-slate-100 space-y-2 text-xs">
              <div className="flex justify-between text-slate-600">
                <span>Profile Completeness:</span>
                <span className="font-bold text-slate-800">{overview?.profile_completeness_percentage || 85}%</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>Completed Roadmap Steps:</span>
                <span className="font-bold text-emerald-600">{overview?.completed_steps_count || 1} of {overview?.total_steps_count || 5}</span>
              </div>
            </div>

            <div className="mt-4">
              <button
                onClick={onExploreAI}
                className="w-full rubick-btn py-2.5 px-4 text-xs font-semibold flex items-center justify-center gap-2"
              >
                <span>Launch Agentic Planning</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Card 2: Mini Realtime Readiness Breakdown (like Rubick Visitors Bar Chart) - 4 cols */}
          <div className="md:col-span-4 rubick-card p-6 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-slate-800">Skill Competencies</span>
                <p className="text-[11px] text-slate-400">Distribution of evaluated topics</p>
              </div>
              <span className="text-xl font-bold text-slate-900">
                {(student?.technical_skills?.length || 4) + (student?.interests?.length || 3)}
              </span>
            </div>

            {/* Mini Bar Chart Graphic matching Rubick */}
            <div className="my-4 flex items-end gap-2 h-24 justify-center">
              {[40, 65, 30, 85, 55, 95, 70, 45, 90].map((h, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <div
                    className="w-full bg-[#1b3bbb] rounded-t-sm transition-all"
                    style={{ height: `${h}%`, opacity: i % 2 === 0 ? 0.9 : 0.4 }}
                  ></div>
                  <span className="text-[9px] text-slate-400">{i + 1}</span>
                </div>
              ))}
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
              <span className="text-slate-500">Curriculum Coverage:</span>
              <span className="font-bold text-[#1b3bbb]">{readinessScore}% Core</span>
            </div>
          </div>

          {/* Card 3: Donut Ring Chart (like Rubick Users By Age) - 3 cols */}
          <div className="md:col-span-3 rubick-card p-6 flex flex-col justify-between">
            <div>
              <span className="text-xs font-bold text-slate-800">Domain Alignment</span>
              <p className="text-[11px] text-slate-400">Technical vs Domain skills</p>
            </div>

            {/* Circular Ring Chart */}
            <div className="my-3 flex items-center justify-center relative">
              <svg className="w-24 h-24 transform -rotate-90">
                <circle cx="48" cy="48" r="38" stroke="#E2E8F0" strokeWidth="8" fill="transparent" />
                <circle
                  cx="48"
                  cy="48"
                  r="38"
                  stroke="#1b3bbb"
                  strokeWidth="8"
                  fill="transparent"
                  strokeDasharray="238"
                  strokeDashoffset={238 - (238 * readinessScore) / 100}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute text-center">
                <span className="text-base font-extrabold text-slate-800">{readinessScore}%</span>
                <p className="text-[9px] text-slate-400 uppercase font-bold">Fit</p>
              </div>
            </div>

            <div className="space-y-1 text-[11px] pt-2 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-slate-600">
                  <span className="w-2 h-2 rounded-full bg-[#1b3bbb]"></span> Technical
                </span>
                <span className="font-bold text-slate-700">75%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-slate-600">
                  <span className="w-2 h-2 rounded-full bg-blue-300"></span> Analytical
                </span>
                <span className="font-bold text-slate-700">25%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* SECTION 2: Blue Promo Banner & Watchlists (matching Rubick middle row) */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-5">
        {/* Blue Promo Banner (like Rubick "Transact safely with Lender's Fund Account") - 5 cols */}
        <div className="md:col-span-5 bg-gradient-to-r from-[#1b3bbb] to-[#152e95] text-white rounded-2xl p-6 flex flex-col justify-between shadow-md relative overflow-hidden">
          <div className="relative z-10">
            <span className="text-[10px] font-bold uppercase tracking-wider bg-white/20 px-2.5 py-0.5 rounded-full inline-block mb-3">
              Explainable Decision Engine
            </span>
            <h3 className="text-lg font-bold leading-snug">
              Decisions Powered by Real Academic Data
            </h3>
            <p className="text-xs text-blue-100 mt-2 leading-relaxed">
              Move beyond guesswork with deterministic scoring, validated prerequisites, and 100% offline curriculum fallback.
            </p>
          </div>

          <div className="mt-6 relative z-10">
            <button
              onClick={onExploreAI}
              className="bg-white text-[#1b3bbb] hover:bg-blue-50 font-bold px-5 py-2 rounded-xl text-xs shadow-sm transition-all flex items-center gap-2"
            >
              <Sparkles className="w-4 h-4 text-[#1b3bbb]" />
              <span>Explore AI Insights</span>
            </button>
          </div>

          {/* Decorative background shape */}
          <div className="absolute -right-8 -bottom-8 w-44 h-44 bg-white/10 rounded-full blur-xl pointer-events-none"></div>
        </div>

        {/* Top Career Roles (like Rubick "Weekly Best Sellers") - 4 cols */}
        <div className="md:col-span-4 rubick-card p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-100">
            <span className="text-xs font-bold text-slate-800">Top Career Matches</span>
            <span className="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-semibold">
              Top 3 Roles
            </span>
          </div>

          <div className="space-y-3">
            {recommendations.slice(0, 3).map((item, idx) => (
              <div
                key={idx}
                onClick={() => onSelectRole(item.career_role.slug)}
                className="flex items-center justify-between p-2 rounded-xl hover:bg-slate-50 transition-all cursor-pointer border border-transparent hover:border-slate-200"
              >
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center text-xs font-extrabold text-[#1b3bbb]">
                    #{idx + 1}
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-800 hover:text-[#1b3bbb] transition-colors leading-tight">
                      {item.career_role.title}
                    </p>
                    <p className="text-[10px] text-slate-400 leading-tight">
                      {item.career_role.category}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-extrabold text-[#1b3bbb] bg-blue-50 px-2 py-0.5 rounded-full border border-blue-100">
                    {item.match_score}%
                  </span>
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={onNavigateToRoadmap}
            className="w-full mt-3 text-center text-xs font-semibold text-[#1b3bbb] hover:underline"
          >
            View Full Curriculum Roadmaps $\rightarrow$
          </button>
        </div>

        {/* Skill Inventory (like Rubick right card) - 3 cols */}
        <div className="md:col-span-3 rubick-card p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-100">
            <span className="text-xs font-bold text-slate-800">Verified Skills</span>
            <span className="text-[10px] text-emerald-600 font-bold bg-emerald-50 px-2 py-0.5 rounded">
              Active
            </span>
          </div>

          <div className="space-y-2">
            {(student?.technical_skills || ['Python', 'SQL', 'Pandas', 'Scikit-Learn']).slice(0, 4).map((skill, i) => (
              <div key={i} className="p-2 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold text-slate-800">{skill}</p>
                  <p className="text-[9px] text-slate-400">Reported Competency</p>
                </div>
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              </div>
            ))}
          </div>

          <div className="mt-3 pt-2 border-t border-slate-100 text-center">
            <span className="text-[11px] text-slate-500 font-medium">
              Self-reported academic inventory
            </span>
          </div>
        </div>
      </div>

      {/* SECTION 3: Performance Curve & Progress Timeline (Rubick Bottom Large Area) */}
      <div className="rubick-card p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h3 className="text-base font-bold text-slate-900 tracking-tight">
              Curriculum Progress & Learning Curve
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Progress tracking across 5 curriculum phases for {targetRoleTitle}
            </p>
          </div>

          {/* Timeframe Buttons matching Rubick (1D, 1W, 1M, 6M, 1Y) */}
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
            {['1D', '1W', '1M', '6M', '1Y'].map((t) => (
              <button
                key={t}
                onClick={() => setTimeFilter(t)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  timeFilter === t
                    ? 'bg-white text-[#1b3bbb] shadow-sm font-bold'
                    : 'text-slate-500 hover:text-slate-800'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* SVG Interactive Progress Chart with Rubick Blue curve */}
        <div className="relative w-full h-48 mt-2">
          <svg viewBox="0 0 900 180" className="w-full h-full overflow-visible">
            <defs>
              <linearGradient id="rubickGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#1b3bbb" stopOpacity="0.2" />
                <stop offset="100%" stopColor="#1b3bbb" stopOpacity="0.0" />
              </linearGradient>
            </defs>

            {/* Clean grid lines */}
            <line x1="0" y1="30" x2="900" y2="30" stroke="#E2E8F0" strokeDasharray="3 3" />
            <line x1="0" y1="80" x2="900" y2="80" stroke="#E2E8F0" strokeDasharray="3 3" />
            <line x1="0" y1="130" x2="900" y2="130" stroke="#E2E8F0" strokeDasharray="3 3" />

            {/* Gradient filled area */}
            <path
              d="M 0 140 Q 150 120 280 95 T 450 50 T 620 75 T 780 110 T 900 60 L 900 180 L 0 180 Z"
              fill="url(#rubickGradient)"
            />

            {/* Solid Royal Blue Curve */}
            <path
              d="M 0 140 Q 150 120 280 95 T 450 50 T 620 75 T 780 110 T 900 60"
              fill="none"
              stroke="#1b3bbb"
              strokeWidth="3.5"
              strokeLinecap="round"
            />

            {/* Interactive Data Point pin */}
            <g transform="translate(450, 50)">
              <line x1="0" y1="0" x2="0" y2="130" stroke="#1b3bbb" strokeDasharray="3 3" opacity="0.5" />
              <circle r="7" fill="#1b3bbb" className="animate-ping opacity-40" />
              <circle r="5" fill="#1b3bbb" stroke="#FFFFFF" strokeWidth="2" />
              <g transform="translate(-65, -45)">
                <rect width="130" height="34" rx="8" fill="#1E293B" />
                <text x="65" y="15" textAnchor="middle" fill="#94A3B8" fontSize="10" fontWeight="500">
                  Active Milestone
                </text>
                <text x="65" y="27" textAnchor="middle" fill="#FFFFFF" fontSize="11" fontWeight="700">
                  {readinessScore}% Readiness
                </text>
              </g>
            </g>
          </svg>

          {/* Month labels */}
          <div className="flex justify-between text-[11px] text-slate-400 font-medium mt-3 px-2">
            <span>Jan</span>
            <span>Feb</span>
            <span>Mar</span>
            <span>Apr</span>
            <span>May</span>
            <span>Jun</span>
            <span>Jul</span>
            <span>Aug</span>
            <span>Sep</span>
            <span>Oct</span>
            <span>Nov</span>
            <span>Dec</span>
          </div>
        </div>
      </div>
    </div>
  );
};
