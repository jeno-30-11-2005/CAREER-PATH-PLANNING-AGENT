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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rubick-card">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-slate-800">Career Compatibility Recommendations</h2>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-blue-50 text-[#1b3bbb] border border-blue-200">
              Deterministic Scoring
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Mathematical matching based on Skills (40%), Interests (30%), Field (15%), Experience (10%), and Goals (5%).
          </p>
        </div>
        <button
          onClick={onRefreshRecommendations}
          disabled={isLoading}
          className="rubick-btn px-5 py-2.5 text-xs font-semibold flex items-center justify-center gap-2 shrink-0"
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
              className="rubick-card p-6 flex flex-col justify-between hover:shadow-rubick-md hover:border-blue-300 transition-all duration-200 group"
            >
              <div>
                {/* Ranking Tag & Match Score */}
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-bold px-3 py-1 rounded-lg bg-slate-100 text-slate-700 border border-slate-200">
                    Match Rank #{idx + 1}
                  </span>
                  <div className="flex items-baseline gap-1 text-right">
                    <span className="text-2xl font-extrabold text-[#1b3bbb]">
                      {item.match_score}%
                    </span>
                    <span className="text-[10px] text-slate-400 font-semibold">Match</span>
                  </div>
                </div>

                <h3 className="text-lg font-bold text-slate-900 group-hover:text-[#1b3bbb] transition-colors">
                  {role.title}
                </h3>
                <p className="text-xs font-semibold text-[#1b3bbb] mt-0.5">{role.category}</p>
                <p className="text-xs text-slate-500 mt-2.5 line-clamp-3 leading-relaxed">
                  {role.description}
                </p>

                {/* Explainable Reasoning */}
                <div className="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-slate-600 leading-relaxed">
                  <p className="font-bold text-slate-800 mb-1">Why this fits:</p>
                  <p>{item.explanation}</p>
                </div>

                {/* Matching Skills */}
                <div className="mt-4">
                  <p className="text-[11px] font-bold text-slate-700 uppercase tracking-wider mb-2">
                    Demonstrated Skills ({item.matching_skills.length})
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {item.matching_skills.length > 0 ? (
                      item.matching_skills.map((s, i) => (
                        <span
                          key={i}
                          className="text-[10px] px-2.5 py-0.5 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-700 font-semibold"
                        >
                          ✓ {s}
                        </span>
                      ))
                    ) : (
                      <span className="text-[10px] text-slate-400 italic">No direct skill matches declared yet.</span>
                    )}
                  </div>
                </div>

                {/* Missing Skills */}
                <div className="mt-4">
                  <p className="text-[11px] font-bold text-slate-700 uppercase tracking-wider mb-2">
                    Priority Gaps to Learn ({item.missing_skills.length})
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {item.missing_skills.slice(0, 4).map((s, i) => (
                      <span
                        key={i}
                        className="text-[10px] px-2.5 py-0.5 rounded-md bg-blue-50 border border-blue-200 text-[#1b3bbb] font-semibold"
                      >
                        + {s}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-6 pt-5 border-t border-slate-100 flex flex-col gap-2">
                <button
                  onClick={() => onSelectRoleForGap(role.slug)}
                  className="w-full rubick-btn-outline py-2.5 px-4 text-xs font-semibold flex items-center justify-center gap-1.5"
                >
                  <span>Skill-Gap Analysis</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => onSelectRoleForRoadmap(role.slug)}
                  className="w-full rubick-btn py-2.5 px-4 text-xs font-semibold flex items-center justify-center gap-1.5"
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
