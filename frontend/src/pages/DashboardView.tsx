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
  Layers
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
  const [watchlistTab, setWatchlistTab] = useState<'top' | 'demand' | 'emerging'>('top');

  const topMatch = recommendations[0];
  const readinessScore = topMatch ? topMatch.match_score : 84.5;
  const targetRoleTitle = overview?.active_roadmap?.target_role || (topMatch ? topMatch.career_role.title : 'AI Engineer');
  const progressPercent = overview?.overall_progress_percentage || 0;

  return (
    <div className="space-y-6">
      {/* Top Grid matching the reference screenshot cards layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Card 1: Total Readiness Metric (styled like "Total Holding $12,304.11") */}
        <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Total Career Readiness</span>
            <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/5 text-[11px] text-slate-300">
              <span>Semester 6</span>
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </div>
          </div>
          <div className="my-4">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white tracking-tight">
                {readinessScore}%
              </span>
              <span className="text-xs font-semibold text-emerald-400 flex items-center">
                +14.2% <ArrowUpRight className="w-3 h-3" />
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">
              Compatibility for <span className="text-white font-medium">{targetRoleTitle}</span>
            </p>
          </div>
          <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-gradient-to-r from-[#9D4EDD] to-[#C77DFF] h-1.5 rounded-full shadow-glow-violet"
              style={{ width: `${readinessScore}%` }}
            ></div>
          </div>
        </div>

        {/* Card 2: "Decisions Powered by Data" Card with Glowing Pill Button */}
        <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6 relative overflow-hidden flex flex-col justify-between">
          <div className="absolute -bottom-8 -left-8 w-40 h-40 bg-purple-600/20 rounded-full blur-2xl pointer-events-none"></div>
          <div>
            <h3 className="text-sm font-bold text-white tracking-tight">
              Decisions Powered by Data
            </h3>
            <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">
              Move beyond guesswork with AI-driven academic analysis tailored to your strengths.
            </p>
          </div>
          <div className="mt-5">
            <button
              onClick={onExploreAI}
              className="w-full neon-btn py-2.5 px-4 rounded-full text-xs font-bold flex items-center justify-center gap-2"
            >
              <Sparkles className="w-4 h-4 text-white" />
              <span>Explore AI Insights</span>
            </button>
          </div>
        </div>

        {/* Card 3: Watchlist / Top Roles (styled like "Watchlist / Spotify, Amazon, NVDA") */}
        <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-white">Target Roles</span>
            {/* Pill tabs: Most Viewed / Gain / Lose */}
            <div className="flex items-center gap-1 bg-[#0B0B0E] p-1 rounded-full border border-white/5 text-[10px]">
              <button
                onClick={() => setWatchlistTab('top')}
                className={`px-2 py-0.5 rounded-full font-medium ${
                  watchlistTab === 'top' ? 'bg-[#1C1C29] text-white' : 'text-slate-400'
                }`}
              >
                Top Matches
              </button>
              <button
                onClick={() => setWatchlistTab('demand')}
                className={`px-2 py-0.5 rounded-full font-medium ${
                  watchlistTab === 'demand' ? 'bg-[#1C1C29] text-white' : 'text-slate-400'
                }`}
              >
                High Demand
              </button>
            </div>
          </div>

          <div className="space-y-2.5">
            {recommendations.slice(0, 3).map((item, idx) => (
              <div
                key={idx}
                onClick={() => onSelectRole(item.career_role.slug)}
                className="flex items-center justify-between p-2 rounded-2xl hover:bg-white/5 transition-all cursor-pointer group"
              >
                <div className="flex items-center gap-2.5">
                  <div className="w-7 h-7 rounded-xl bg-purple-950/40 border border-purple-500/20 flex items-center justify-center text-xs font-bold text-[#E0AAFF]">
                    {idx + 1}
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-white group-hover:text-[#C77DFF] transition-colors leading-tight">
                      {item.career_role.title}
                    </p>
                    <p className="text-[10px] text-slate-500 leading-tight">
                      {item.career_role.category}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold text-[#E0AAFF]">{item.match_score}%</p>
                  <p className="text-[10px] text-emerald-400 font-semibold">+Match</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Card 4: My Skills Portfolio (styled like "My Portfolio AAPL, AMZN, NVDA") */}
        <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-white">Skill Inventory</span>
            <button
              onClick={onNavigateToRoadmap}
              className="text-[11px] text-[#C77DFF] hover:underline flex items-center gap-0.5"
            >
              See all <ArrowUpRight className="w-3 h-3" />
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2.5">
            {(student?.technical_skills || ['Python', 'SQL', 'Pandas', 'Scikit-Learn']).slice(0, 4).map((skill, i) => (
              <div key={i} className="bg-[#0D0D14] border border-white/5 rounded-2xl p-2.5">
                <p className="text-xs font-bold text-white leading-tight">{skill}</p>
                <p className="text-[10px] text-emerald-400 font-semibold mt-0.5">Verified 100%</p>
                <p className="text-[9px] text-slate-500 mt-1">Core Tech</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Large Card: Performance Curve / Readiness Timeline matching reference */}
      <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">
              Curriculum Progress & Readiness Curve
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Cumulative mastery tracking based on completed roadmap milestones
            </p>
          </div>

          {/* Timeframe Buttons (1D, 1W, 1M, 6M, 1Y) matching the reference screenshot */}
          <div className="flex items-center gap-1.5 bg-[#0B0B0E] p-1 rounded-full border border-white/5">
            {['1D', '1W', '1M', '6M', '1Y'].map((t) => (
              <button
                key={t}
                onClick={() => setTimeFilter(t)}
                className={`px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                  timeFilter === t
                    ? 'bg-[#1C1C29] text-white border border-purple-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* SVG Interactive Wave Chart matching reference graph */}
        <div className="relative w-full h-52 mt-4">
          <svg viewBox="0 0 900 200" className="w-full h-full overflow-visible">
            <defs>
              <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#9D4EDD" stopOpacity="0.4" />
                <stop offset="100%" stopColor="#9D4EDD" stopOpacity="0.0" />
              </linearGradient>
            </defs>
            {/* Soft grid lines */}
            <line x1="0" y1="40" x2="900" y2="40" stroke="rgba(255,255,255,0.04)" strokeDasharray="4 4" />
            <line x1="0" y1="90" x2="900" y2="90" stroke="rgba(255,255,255,0.04)" strokeDasharray="4 4" />
            <line x1="0" y1="140" x2="900" y2="140" stroke="rgba(255,255,255,0.04)" strokeDasharray="4 4" />

            {/* Filled area */}
            <path
              d="M 0 160 Q 150 140 280 110 T 450 60 T 620 90 T 780 130 T 900 70 L 900 200 L 0 200 Z"
              fill="url(#chartGradient)"
            />
            {/* Glowing path curve */}
            <path
              d="M 0 160 Q 150 140 280 110 T 450 60 T 620 90 T 780 130 T 900 70"
              fill="none"
              stroke="#C77DFF"
              strokeWidth="3.5"
              strokeLinecap="round"
            />

            {/* Interactive Data Point pin matching the reference screenshot */}
            <g transform="translate(450, 60)">
              <line x1="0" y1="0" x2="0" y2="140" stroke="#E0AAFF" strokeDasharray="3 3" opacity="0.6" />
              <circle r="7" fill="#E0AAFF" className="animate-ping opacity-75" />
              <circle r="6" fill="#9D4EDD" stroke="#FFFFFF" strokeWidth="2.5" />
              <g transform="translate(-60, -50)">
                <rect width="120" height="36" rx="10" fill="#1C1C28" stroke="rgba(255,255,255,0.15)" />
                <text x="60" y="16" textAnchor="middle" fill="#94A3B8" fontSize="10" fontWeight="500">
                  Current Milestone
                </text>
                <text x="60" y="30" textAnchor="middle" fill="#FFFFFF" fontSize="11" fontWeight="700">
                  {readinessScore}% Readiness
                </text>
              </g>
            </g>
          </svg>

          {/* Month labels */}
          <div className="flex justify-between text-[11px] text-slate-500 font-medium mt-3 px-2">
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
