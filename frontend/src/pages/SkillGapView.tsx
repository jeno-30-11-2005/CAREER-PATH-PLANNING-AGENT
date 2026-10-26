import React from 'react';
import { GitMerge, CheckCircle2, Clock, AlertCircle, ArrowRight, Sparkles, BookOpen } from 'lucide-react';
import { CareerRole, SkillGapResponse } from '../types';

interface SkillGapViewProps {
  roles: CareerRole[];
  selectedRoleSlug: string;
  onSelectRole: (slug: string) => void;
  gapData: SkillGapResponse | null;
  onGenerateRoadmap: (roleSlug: string) => void;
  isLoading: boolean;
}

export const SkillGapView: React.FC<SkillGapViewProps> = ({
  roles,
  selectedRoleSlug,
  onSelectRole,
  gapData,
  onGenerateRoadmap,
  isLoading
}) => {
  return (
    <div className="space-y-6">
      {/* Top Selector Banner */}
      <div className="p-6 rubick-card flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <GitMerge className="w-5 h-5 text-[#1b3bbb]" />
            <span>Skill-Gap Matrix & Analysis</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Compare your self-reported skills against curated industry & academic curricula
          </p>
        </div>

        {/* Role Selector Dropdown */}
        <div className="flex items-center gap-3">
          <label className="text-xs font-bold text-slate-600">Target Role:</label>
          <select
            value={selectedRoleSlug}
            onChange={(e) => onSelectRole(e.target.value)}
            className="bg-slate-50 border border-slate-300 rounded-xl px-4 py-2 text-xs font-semibold text-slate-800 focus:outline-none focus:border-[#1b3bbb] transition-all shadow-sm"
          >
            {roles.map((r) => (
              <option key={r.slug} value={r.slug}>
                {r.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Educational Disclaimer Alert */}
      {gapData?.disclaimer && (
        <div className="p-4 rounded-xl bg-blue-50 border border-blue-200 flex items-start gap-3">
          <AlertCircle className="w-4 h-4 text-[#1b3bbb] shrink-0 mt-0.5" />
          <p className="text-xs text-blue-900 leading-relaxed font-medium">
            {gapData.disclaimer}
          </p>
        </div>
      )}

      {/* Metric Counters */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="rubick-card p-5">
          <p className="text-xs text-slate-500 font-medium">Total Curriculum Skills</p>
          <p className="text-2xl font-extrabold text-slate-900 mt-1">
            {gapData?.total_required_skills || 0}
          </p>
        </div>
        <div className="rubick-card border-l-4 border-l-emerald-500 p-5">
          <p className="text-xs text-emerald-600 font-semibold">Already Reported</p>
          <p className="text-2xl font-extrabold text-emerald-700 mt-1">
            {gapData?.confirmed_skills.length || 0}
          </p>
        </div>
        <div className="rubick-card border-l-4 border-l-amber-500 p-5">
          <p className="text-xs text-amber-600 font-semibold">Partially Developed</p>
          <p className="text-2xl font-extrabold text-amber-700 mt-1">
            {gapData?.partially_developed_skills.length || 0}
          </p>
        </div>
        <div className="rubick-card border-l-4 border-l-[#1b3bbb] p-5">
          <p className="text-xs text-[#1b3bbb] font-semibold">Not Yet Reported</p>
          <p className="text-2xl font-extrabold text-[#1b3bbb] mt-1">
            {gapData?.not_yet_reported_skills.length || 0}
          </p>
        </div>
      </div>

      {/* Three Column Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Column 1: Confirmed Skills */}
        <div className="rubick-card p-6">
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <h3 className="text-sm font-bold text-slate-900">Confirmed (Reported)</h3>
          </div>
          <div className="space-y-2">
            {gapData?.confirmed_skills.length ? (
              gapData.confirmed_skills.map((skill, i) => (
                <div
                  key={i}
                  className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-between text-xs"
                >
                  <span className="font-bold text-emerald-900">{skill}</span>
                  <span className="text-[10px] text-emerald-700 font-bold px-2 py-0.5 rounded bg-emerald-100">
                    Active
                  </span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-400 italic p-3">No matching skills reported yet.</p>
            )}
          </div>
        </div>

        {/* Column 2: Partially Developed Skills */}
        <div className="rubick-card p-6">
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
            <Clock className="w-4 h-4 text-amber-600" />
            <h3 className="text-sm font-bold text-slate-900">Partially Developed</h3>
          </div>
          <div className="space-y-2">
            {gapData?.partially_developed_skills.length ? (
              gapData.partially_developed_skills.map((skill, i) => (
                <div
                  key={i}
                  className="p-3 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-between text-xs"
                >
                  <span className="font-bold text-amber-900">{skill}</span>
                  <span className="text-[10px] text-amber-700 font-bold px-2 py-0.5 rounded bg-amber-100">
                    Needs Depth
                  </span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-400 italic p-3">No partial skills identified.</p>
            )}
          </div>
        </div>

        {/* Column 3: Not Yet Reported */}
        <div className="rubick-card p-6">
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
            <AlertCircle className="w-4 h-4 text-[#1b3bbb]" />
            <h3 className="text-sm font-bold text-slate-900">Not Yet Reported</h3>
          </div>
          <div className="space-y-2">
            {gapData?.not_yet_reported_skills.length ? (
              gapData.not_yet_reported_skills.map((skill, i) => (
                <div
                  key={i}
                  className="p-3 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-between text-xs"
                >
                  <span className="font-bold text-blue-900">{skill}</span>
                  <span className="text-[10px] text-[#1b3bbb] font-bold px-2 py-0.5 rounded bg-blue-100">
                    To Learn
                  </span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-400 italic p-3">All target skills reported!</p>
            )}
          </div>
        </div>
      </div>

      {/* Recommended Learning Order & CTA */}
      <div className="rubick-card p-6 sm:p-8 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h3 className="text-sm font-bold text-slate-900 mb-1">
            Recommended Prioritized Learning Order:
          </h3>
          <div className="flex flex-wrap gap-2 mt-2">
            {gapData?.recommended_learning_order.map((skill, index) => (
              <span
                key={index}
                className="text-xs px-3 py-1 rounded-lg bg-slate-100 border border-slate-200 text-slate-800 font-medium flex items-center gap-1.5"
              >
                <span className="w-4 h-4 rounded-full bg-[#1b3bbb] text-white text-[10px] font-bold flex items-center justify-center">
                  {index + 1}
                </span>
                {skill}
              </span>
            ))}
          </div>
        </div>

        <button
          onClick={() => onGenerateRoadmap(selectedRoleSlug)}
          className="rubick-btn px-6 py-3 text-xs font-semibold flex items-center gap-2 shrink-0"
        >
          <Sparkles className="w-4 h-4" />
          <span>Generate Roadmap for {gapData?.career_role_title || 'Role'}</span>
        </button>
      </div>
    </div>
  );
};
