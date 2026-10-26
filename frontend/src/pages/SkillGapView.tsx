import React, { useState, useEffect } from 'react';
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
      <div className="p-6 bg-[#14141D] border border-white/5 rounded-3xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <GitMerge className="w-5 h-5 text-[#C77DFF]" />
            <span>Skill-Gap Matrix & Analysis</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Compare your self-reported skills against curated industry & academic curricula
          </p>
        </div>

        {/* Role Selector Dropdown */}
        <div className="flex items-center gap-3">
          <label className="text-xs font-semibold text-slate-400">Target Role:</label>
          <select
            value={selectedRoleSlug}
            onChange={(e) => onSelectRole(e.target.value)}
            className="bg-[#1C1C28] border border-white/10 rounded-2xl px-4 py-2 text-xs font-semibold text-white focus:outline-none focus:border-purple-500 transition-all"
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
        <div className="p-4 rounded-2xl bg-purple-950/20 border border-purple-500/20 flex items-start gap-3">
          <AlertCircle className="w-4 h-4 text-[#C77DFF] shrink-0 mt-0.5" />
          <p className="text-xs text-purple-200/80 leading-relaxed">
            {gapData.disclaimer}
          </p>
        </div>
      )}

      {/* Metric Counters */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="bg-[#14141D] border border-white/5 rounded-2xl p-5">
          <p className="text-xs text-slate-400 font-medium">Total Curriculum Skills</p>
          <p className="text-2xl font-bold text-white mt-1">
            {gapData?.total_required_skills || 0}
          </p>
        </div>
        <div className="bg-[#14141D] border border-emerald-500/20 rounded-2xl p-5">
          <p className="text-xs text-emerald-400 font-medium">Already Reported</p>
          <p className="text-2xl font-bold text-emerald-300 mt-1">
            {gapData?.confirmed_skills.length || 0}
          </p>
        </div>
        <div className="bg-[#14141D] border border-amber-500/20 rounded-2xl p-5">
          <p className="text-xs text-amber-400 font-medium">Partially Developed</p>
          <p className="text-2xl font-bold text-amber-300 mt-1">
            {gapData?.partially_developed_skills.length || 0}
          </p>
        </div>
        <div className="bg-[#14141D] border border-purple-500/20 rounded-2xl p-5">
          <p className="text-xs text-purple-400 font-medium">Not Yet Reported</p>
          <p className="text-2xl font-bold text-[#E0AAFF] mt-1">
            {gapData?.not_yet_reported_skills.length || 0}
          </p>
        </div>
      </div>

      {/* Three Column Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Column 1: Confirmed Skills */}
        <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6">
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-white/5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-white">Confirmed (Reported)</h3>
          </div>
          <div className="space-y-2">
            {gapData?.confirmed_skills.length ? (
              gapData.confirmed_skills.map((skill, i) => (
                <div
                  key={i}
                  className="p-3 rounded-2xl bg-emerald-950/20 border border-emerald-500/20 flex items-center justify-between text-xs"
                >
                  <span className="font-semibold text-emerald-200">{skill}</span>
                  <span className="text-[10px] text-emerald-400 font-semibold px-2 py-0.5 rounded-full bg-emerald-900/30">
                    Active
                  </span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 italic p-3">No matching skills reported yet.</p>
            )}
          </div>
        </div>

        {/* Column 2: Partially Developed Skills */}
        <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6">
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-white/5">
            <Clock className="w-4 h-4 text-amber-400" />
            <h3 className="text-sm font-bold text-white">Partially Developed</h3>
          </div>
          <div className="space-y-2">
            {gapData?.partially_developed_skills.length ? (
              gapData.partially_developed_skills.map((skill, i) => (
                <div
                  key={i}
                  className="p-3 rounded-2xl bg-amber-950/20 border border-amber-500/20 flex items-center justify-between text-xs"
                >
                  <span className="font-semibold text-amber-200">{skill}</span>
                  <span className="text-[10px] text-amber-400 font-semibold px-2 py-0.5 rounded-full bg-amber-900/30">
                    Needs Depth
                  </span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 italic p-3">No partial skills identified.</p>
            )}
          </div>
        </div>

        {/* Column 3: Not Yet Reported */}
        <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6">
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-white/5">
            <AlertCircle className="w-4 h-4 text-[#C77DFF]" />
            <h3 className="text-sm font-bold text-white">Not Yet Reported</h3>
          </div>
          <div className="space-y-2">
            {gapData?.not_yet_reported_skills.length ? (
              gapData.not_yet_reported_skills.map((skill, i) => (
                <div
                  key={i}
                  className="p-3 rounded-2xl bg-purple-950/20 border border-purple-500/20 flex items-center justify-between text-xs"
                >
                  <span className="font-semibold text-purple-200">{skill}</span>
                  <span className="text-[10px] text-[#E0AAFF] font-semibold px-2 py-0.5 rounded-full bg-purple-900/40">
                    To Learn
                  </span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 italic p-3">All target skills reported!</p>
            )}
          </div>
        </div>
      </div>

      {/* Recommended Learning Order & CTA */}
      <div className="bg-[#14141D] border border-white/5 rounded-3xl p-6 sm:p-8 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h3 className="text-sm font-bold text-white mb-1">
            Recommended Prioritized Learning Order:
          </h3>
          <div className="flex flex-wrap gap-2 mt-2">
            {gapData?.recommended_learning_order.map((skill, index) => (
              <span
                key={index}
                className="text-xs px-3 py-1 rounded-full bg-[#1C1C28] border border-white/10 text-slate-200 flex items-center gap-1.5"
              >
                <span className="w-4 h-4 rounded-full bg-purple-500/30 text-[#E0AAFF] text-[10px] font-bold flex items-center justify-center">
                  {index + 1}
                </span>
                {skill}
              </span>
            ))}
          </div>
        </div>

        <button
          onClick={() => onGenerateRoadmap(selectedRoleSlug)}
          className="neon-btn px-6 py-3 rounded-full text-xs font-bold flex items-center gap-2 shrink-0"
        >
          <Sparkles className="w-4 h-4" />
          <span>Generate Roadmap for {gapData?.career_role_title || 'Role'}</span>
        </button>
      </div>
    </div>
  );
};
