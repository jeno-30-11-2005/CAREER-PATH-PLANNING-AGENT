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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div className="bg-white border border-slate-200 rounded-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto shadow-2xl p-6 sm:p-8">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-[#1b3bbb]">
              <Sparkles className="w-5 h-5 text-[#1b3bbb]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-slate-900">Agentic Workflow: Plan Proposal</h2>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-blue-50 text-[#1b3bbb] border border-blue-200">
                  Human-in-the-Loop
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Coordinated pipeline executed across 5 analytical components
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-500 hover:text-slate-800 transition-all"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Workflow Execution Log Stepper */}
        <div className="mt-5 bg-slate-50 border border-slate-200 rounded-xl p-4">
          <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2.5">
            Component Coordination Pipeline
          </h3>
          <div className="space-y-1.5 font-mono text-[11px] text-slate-700">
            {workflowData.workflow_log.map((log, index) => (
              <div key={index} className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                <span>{log}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Quality Review & Guardrails Check */}
        <div className="mt-4 p-4 rounded-xl bg-emerald-50 border border-emerald-200">
          <div className="flex items-center gap-2 text-emerald-800 font-bold text-xs mb-1">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Component 5: Quality Review & Guardrail Verification (Passed)</span>
          </div>
          <div className="grid grid-cols-2 gap-2 text-[11px] text-emerald-900 mt-2">
            {workflowData.quality_review.checks_run.map((check, idx) => (
              <div key={idx} className="flex items-center gap-1.5">
                <span className="text-emerald-600 font-bold">✓</span> {check}
              </div>
            ))}
          </div>
        </div>

        {/* Proposed Target Role & Roadmap Preview */}
        <div className="mt-5 space-y-4">
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider">Target Career Role</p>
              <h4 className="text-base font-bold text-slate-900 mt-0.5">
                {workflowData.selected_role.title}
              </h4>
              <p className="text-xs font-semibold text-[#1b3bbb]">{workflowData.selected_role.category}</p>
            </div>
            <div className="text-right">
              <p className="text-[11px] text-slate-500">Curriculum Scope</p>
              <p className="text-base font-bold text-slate-900">
                {workflowData.proposed_roadmap.items.length} Milestones
              </p>
              <p className="text-xs text-slate-500">
                ~{workflowData.proposed_roadmap.total_estimated_weeks} Weeks ({workflowData.proposed_roadmap.weekly_hours} hrs/wk)
              </p>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Proposed Curriculum Steps (Awaiting Approval)
            </h4>
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {workflowData.proposed_roadmap.items.map((step, idx) => (
                <div
                  key={idx}
                  className="bg-white border border-slate-200 rounded-xl p-3 flex items-start justify-between text-xs shadow-sm"
                >
                  <div>
                    <span className="font-bold text-slate-900">
                      {step.step_number}. {step.skill_topic}
                    </span>
                    <p className="text-[11px] text-slate-500 mt-0.5">{step.why_it_matters}</p>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-blue-50 text-[#1b3bbb] font-bold shrink-0 ml-3 border border-blue-100">
                    {step.phase.split('.')[1] || step.phase}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Human in the loop confirmation footer */}
        <div className="flex items-center justify-between pt-5 mt-5 border-t border-slate-200">
          <p className="text-xs text-slate-500 italic">
            * You can modify milestones and track progress anytime after approval.
          </p>
          <div className="flex items-center gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-all"
            >
              Cancel
            </button>
            <button
              onClick={onApprove}
              disabled={isApproving}
              className="rubick-btn px-5 py-2 text-xs font-semibold flex items-center gap-2"
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
