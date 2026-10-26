import React from 'react';
import { RecommendationItem } from '../types';
import { Compass, CheckCircle2, AlertCircle, ArrowRight, Sparkles, BookOpen } from 'lucide-react';

interface RecommendationsViewProps {
  recommendations: RecommendationItem[];
  onSelectRoleForGap: (slug: string) => void;
  onSelectRoleForRoadmap: (slug: string) => void;
  onRefreshRecommendations: () => void;
  isLoading: boolean;
}

export const RecommendationsView: React.FC<RecommendationsViewProps> = ({
  recommendations,
  onSelectRoleForGap,
  onSelectRoleForRoadmap,
  onRefreshRecommendations,
  isLoading
}) => {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 bg-[#14141D] border border-white/5 rounded-3xl">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white">Career Compatibility Recommendations</h2>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-purple-500/20 text-[#E0AAFF] border border-purple-500/30">
              Deterministic Scoring
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Weighted matching based on your declared technical skills (40%), interests (30%), field preference (15%), experience (10%), and goals (5%).
          </p>
        </div>
        <button
          onClick={onRefreshRecommendations}
          disabled={isLoading}
          className="neon-btn px-5 py-2.5 rounded-full text-xs font-bold flex items-center justify-center gap-2 shrink-0"
        >
          <Sparkles className="w-4 h-4" />
          <span>{isLoading ? 'Recomputing...' : 'Recompute Scores'}</span>
        </button>
      </div>

      {/* Recommendations Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {recommendations.map((item, idx) => {
          const role = item.career_role;
          return (
            <div
              key={role.slug}
              className="bg-[#14141D] border border-white/5 hover:border-purple-500/30 rounded-3xl p-6 flex flex-col justify-between transition-all duration-300 hover:shadow-glow-violet group"
            >
              <div>
                {/* Ranking Tag & Match Score */}
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-bold px-3 py-1 rounded-full bg-white/5 text-slate-300 border border-white/5">
                    Match Rank #{idx + 1}
                  </span>
                  <div className="flex items-baseline gap-1 text-right">
                    <span className="text-2xl font-extrabold text-[#E0AAFF] group-hover:scale-105 transition-transform">
                      {item.match_score}%
                    </span>
                    <span className="text-[10px] text-slate-400 font-semibold">Match</span>
                  </div>
                </div>

                <h3 className="text-lg font-bold text-white group-hover:text-[#C77DFF] transition-colors">
                  {role.title}
                </h3>
                <p className="text-xs font-semibold text-purple-400 mt-0.5">{role.category}</p>
                <p className="text-xs text-slate-400 mt-2.5 line-clamp-3 leading-relaxed">
                  {role.description}
                </p>

                {/* Explainable Reasoning */}
                <div className="mt-4 p-3 rounded-2xl bg-[#0B0B0E] border border-white/5 text-[11px] text-slate-300 leading-relaxed">
                  <p className="font-semibold text-white mb-1">Why this fits:</p>
                  <p>{item.explanation}</p>
                </div>

                {/* Matching Skills */}
                <div className="mt-4">
                  <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Demonstrated Skills ({item.matching_skills.length})
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {item.matching_skills.length > 0 ? (
                      item.matching_skills.map((s, i) => (
                        <span
                          key={i}
                          className="text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 font-medium"
                        >
                          ✓ {s}
                        </span>
                      ))
                    ) : (
                      <span className="text-[10px] text-slate-500 italic">No direct skill matches declared yet.</span>
                    )}
                  </div>
                </div>

                {/* Missing Skills */}
                <div className="mt-4">
                  <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Priority Gaps to Learn ({item.missing_skills.length})
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {item.missing_skills.slice(0, 4).map((s, i) => (
                      <span
                        key={i}
                        className="text-[10px] px-2.5 py-0.5 rounded-full bg-purple-950/30 border border-purple-500/20 text-[#E0AAFF] font-medium"
                      >
                        + {s}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-6 pt-5 border-t border-white/5 flex flex-col gap-2">
                <button
                  onClick={() => onSelectRoleForGap(role.slug)}
                  className="w-full py-2.5 px-4 rounded-full text-xs font-semibold bg-[#1C1C28] hover:bg-[#252538] text-white border border-white/10 flex items-center justify-center gap-1.5 transition-all"
                >
                  <span>Skill-Gap Analysis</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => onSelectRoleForRoadmap(role.slug)}
                  className="w-full neon-btn py-2.5 px-4 rounded-full text-xs font-semibold flex items-center justify-center gap-1.5"
                >
                  <Sparkles className="w-3.5 h-3.5 text-white" />
                  <span>Build Learning Roadmap</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
