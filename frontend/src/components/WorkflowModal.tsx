import React from 'react';
import { CheckCircle2, AlertTriangle, ShieldCheck, ArrowRight, X, Sparkles } from 'lucide-react';
import { WorkflowResult } from '../types';

interface WorkflowModalProps {
  isOpen: boolean;
  onClose: () => void;
  workflowData: WorkflowResult | null;
  onApprove: () => void;
  isApproving: boolean;
}

export const WorkflowModal: React.FC<WorkflowModalProps> = ({
  isOpen,
  onClose,
  workflowData,
  onApprove,
  isApproving
}) => {
  if (!isOpen || !workflowData) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
      <div className="bg-[#12121A] border border-purple-500/30 rounded-3xl w-full max-w-3xl max-h-[90vh] overflow-y-auto shadow-glow-violet p-6 sm:p-8">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-white/5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#9D4EDD] to-[#C77DFF] flex items-center justify-center shadow-glow-violet">
              <Sparkles className="w-5 h-5 text-white animate-spin-slow" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-white">Agentic Workflow: Plan Proposal</h2>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-purple-500/20 text-[#E0AAFF] border border-purple-500/30">
                  Human-in-the-Loop
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Coordinated pipeline executed across 5 analytical components
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-9 h-9 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-slate-400 hover:text-white transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Workflow Execution Log Stepper */}
        <div className="mt-5 bg-[#0B0B0E] border border-white/5 rounded-2xl p-4">
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2.5">
            Component Coordination Pipeline
          </h3>
          <div className="space-y-1.5 font-mono text-[11px] text-slate-300">
            {workflowData.workflow_log.map((log, index) => (
              <div key={index} className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>{log}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Quality Review & Guardrails Check */}
        <div className="mt-4 p-4 rounded-2xl bg-emerald-950/20 border border-emerald-500/30">
          <div className="flex items-center gap-2 text-emerald-400 font-semibold text-xs mb-1">
            <ShieldCheck className="w-4 h-4" />
            <span>Component 5: Quality Review & Guardrail Verification (Passed)</span>
          </div>
          <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-300 mt-2">
            {workflowData.quality_review.checks_run.map((check, idx) => (
              <div key={idx} className="flex items-center gap-1.5">
                <span className="text-emerald-400">✓</span> {check}
              </div>
            ))}
          </div>
        </div>

        {/* Proposed Target Role & Roadmap Preview */}
        <div className="mt-5 space-y-4">
          <div className="bg-[#181822] border border-white/5 rounded-2xl p-4 flex items-center justify-between">
            <div>
              <p className="text-[11px] text-slate-400 uppercase tracking-wider">Target Career Role</p>
              <h4 className="text-base font-bold text-white mt-0.5">
                {workflowData.selected_role.title}
              </h4>
              <p className="text-xs text-[#C77DFF]">{workflowData.selected_role.category}</p>
            </div>
            <div className="text-right">
              <p className="text-[11px] text-slate-400">Curriculum Scope</p>
              <p className="text-base font-bold text-white">
                {workflowData.proposed_roadmap.items.length} Milestones
              </p>
              <p className="text-xs text-slate-400">
                ~{workflowData.proposed_roadmap.total_estimated_weeks} Weeks ({workflowData.proposed_roadmap.weekly_hours} hrs/wk)
              </p>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Proposed Curriculum Steps (Awaiting Approval)
            </h4>
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {workflowData.proposed_roadmap.items.map((step, idx) => (
                <div
                  key={idx}
                  className="bg-[#161620] border border-white/5 rounded-xl p-3 flex items-start justify-between text-xs"
                >
                  <div>
                    <span className="font-semibold text-white">
                      {step.step_number}. {step.skill_topic}
                    </span>
                    <p className="text-[11px] text-slate-400 mt-0.5">{step.why_it_matters}</p>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-white/5 text-slate-300 shrink-0 ml-3">
                    {step.phase.split('.')[1] || step.phase}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Human in the loop confirmation footer */}
        <div className="flex items-center justify-between pt-6 mt-6 border-t border-white/5">
          <p className="text-xs text-slate-400 italic">
            * You can modify milestones and track progress anytime after approval.
          </p>
          <div className="flex items-center gap-3">
            <button
              onClick={onClose}
              className="px-5 py-2.5 rounded-full text-xs font-semibold text-slate-400 hover:text-white hover:bg-white/5 transition-all"
            >
              Cancel
            </button>
            <button
              onClick={onApprove}
              disabled={isApproving}
              className="neon-btn px-6 py-2.5 rounded-full text-xs font-semibold flex items-center gap-2"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>{isApproving ? 'Saving...' : 'Approve & Commit Plan'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
