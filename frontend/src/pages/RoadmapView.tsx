import React, { useState } from 'react';
import {
  MapPin,
  CheckCircle2,
  Clock,
  ExternalLink,
  BookOpen,
  ChevronDown,
  ChevronUp,
  Save,
  Sparkles,
  Layers,
  Target
} from 'lucide-react';
import { LearningRoadmap, RoadmapItem } from '../types';

interface RoadmapViewProps {
  roadmap: LearningRoadmap | null;
  onUpdateItem: (itemId: number, status: string, notes: string) => Promise<void>;
  onTriggerAgentWorkflow: () => void;
  isLoading: boolean;
}

export const RoadmapView: React.FC<RoadmapViewProps> = ({
  roadmap,
  onUpdateItem,
  onTriggerAgentWorkflow,
  isLoading
}) => {
  const [expandedSteps, setExpandedSteps] = useState<Record<number, boolean>>({});
  const [notesState, setNotesState] = useState<Record<number, string>>({});
  const [savingItem, setSavingItem] = useState<number | null>(null);

  if (!roadmap || !roadmap.items || roadmap.items.length === 0) {
    return (
      <div className="rubick-card p-12 text-center space-y-4">
        <div className="w-14 h-14 rounded-2xl bg-blue-50 border border-blue-200 flex items-center justify-center text-[#1b3bbb] mx-auto">
          <MapPin className="w-7 h-7" />
        </div>
        <h3 className="text-lg font-bold text-slate-900">No Active Career Roadmap Found</h3>
        <p className="text-xs text-slate-500 max-w-md mx-auto">
          Run the agentic planning workflow to generate a personalized 5-phase curriculum tailored to your background and weekly study hours.
        </p>
        <button
          onClick={onTriggerAgentWorkflow}
          className="rubick-btn px-6 py-3 text-xs font-semibold inline-flex items-center gap-2"
        >
          <Sparkles className="w-4 h-4" />
          <span>Launch Agentic Planning Workflow</span>
        </button>
      </div>
    );
  }

  const toggleExpand = (stepNumber: number) => {
    setExpandedSteps((prev) => ({ ...prev, [stepNumber]: !prev[stepNumber] }));
  };

  const handleStatusChange = async (item: RoadmapItem, newStatus: string) => {
    if (!item.id) return;
    const currentNotes = notesState[item.id] !== undefined ? notesState[item.id] : item.learning_notes || '';
    await onUpdateItem(item.id, newStatus, currentNotes);
  };

  const handleSaveNotes = async (item: RoadmapItem) => {
    if (!item.id) return;
    setSavingItem(item.id);
    const currentNotes = notesState[item.id] !== undefined ? notesState[item.id] : item.learning_notes || '';
    await onUpdateItem(item.id, item.completion_status, currentNotes);
    setSavingItem(null);
  };

  // Group items by phase
  const groupedPhases: Record<string, RoadmapItem[]> = {};
  roadmap.items.forEach((item) => {
    if (!groupedPhases[item.phase]) {
      groupedPhases[item.phase] = [];
    }
    groupedPhases[item.phase].push(item);
  });

  const totalSteps = roadmap.items.length;
  const completedSteps = roadmap.items.filter((i) => i.completion_status === 'completed').length;
  const progressPercent = Math.round((completedSteps / totalSteps) * 100);

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 sm:p-8 rubick-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-blue-50 text-[#1b3bbb] border border-blue-200">
              Active Roadmap
            </span>
            <span className="text-xs text-slate-500">
              Estimated: ~{roadmap.total_estimated_weeks} Weeks ({roadmap.weekly_hours} hrs/week)
            </span>
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 mt-1.5">{roadmap.title}</h2>
          <p className="text-xs text-slate-500 mt-1">
            Structured into 5 progressive phases: Foundations $\rightarrow$ Core Skills $\rightarrow$ Applied Practice $\rightarrow$ Portfolio Projects $\rightarrow$ Viva Prep.
          </p>
        </div>

        {/* Progress Summary Card */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 sm:min-w-[220px]">
          <div className="flex items-center justify-between text-xs mb-1.5">
            <span className="text-slate-600 font-semibold">Overall Progress</span>
            <span className="text-sm font-bold text-[#1b3bbb]">{progressPercent}%</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden mb-2">
            <div
              className="bg-[#1b3bbb] h-2 rounded-full transition-all duration-500"
              style={{ width: `${progressPercent}%` }}
            ></div>
          </div>
          <p className="text-[10px] text-slate-500">
            {completedSteps} of {totalSteps} milestones marked completed
          </p>
        </div>
      </div>

      {/* 5-Phases Accordion Stepper */}
      <div className="space-y-6">
        {Object.entries(groupedPhases).map(([phaseName, phaseItems], phaseIndex) => (
          <div key={phaseName} className="rubick-card p-6">
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-xs font-extrabold text-[#1b3bbb]">
                  {phaseIndex + 1}
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">{phaseName}</h3>
                  <p className="text-[11px] text-slate-400">
                    {phaseItems.length} Milestones •{' '}
                    {phaseItems.reduce((acc, curr) => acc + curr.estimated_effort_hours, 0)} Total Hours
                  </p>
                </div>
              </div>
            </div>

            {/* Step Cards within Phase */}
            <div className="space-y-3">
              {phaseItems.map((item) => {
                const isExpanded = expandedSteps[item.step_number] ?? true;
                const isCompleted = item.completion_status === 'completed';
                const isInProgress = item.completion_status === 'in_progress';
                const noteVal = notesState[item.id!] !== undefined ? notesState[item.id!] : item.learning_notes || '';

                return (
                  <div
                    key={item.step_number}
                    className={`rounded-xl border transition-all ${
                      isCompleted
                        ? 'bg-emerald-50/50 border-emerald-200'
                        : isInProgress
                        ? 'bg-blue-50/50 border-blue-200 shadow-sm'
                        : 'bg-white border-slate-200'
                    }`}
                  >
                    {/* Step Summary Bar */}
                    <div className="p-4 flex items-center justify-between gap-4">
                      <div className="flex items-center gap-3.5">
                        {/* Status Select Toggle */}
                        <select
                          value={item.completion_status}
                          onChange={(e) => handleStatusChange(item, e.target.value)}
                          className={`text-xs font-semibold px-3 py-1.5 rounded-lg border focus:outline-none transition-all shadow-sm ${
                            isCompleted
                              ? 'bg-emerald-100 border-emerald-300 text-emerald-800'
                              : isInProgress
                              ? 'bg-blue-100 border-blue-300 text-[#1b3bbb]'
                              : 'bg-slate-50 border-slate-300 text-slate-700'
                          }`}
                        >
                          <option value="not_started">⚪ Not Started</option>
                          <option value="in_progress">🔵 In Progress</option>
                          <option value="completed">🟢 Completed</option>
                        </select>

                        <div>
                          <h4
                            className={`text-sm font-bold ${
                              isCompleted ? 'text-slate-500 line-through' : 'text-slate-900'
                            }`}
                          >
                            {item.step_number}. {item.skill_topic}
                          </h4>
                          <p className="text-[11px] text-slate-500 mt-0.5">{item.why_it_matters}</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="text-[11px] text-slate-500 hidden sm:inline-flex items-center gap-1 font-medium">
                          <Clock className="w-3.5 h-3.5 text-slate-400" />
                          {item.estimated_effort_hours}h effort
                        </span>
                        <button
                          onClick={() => toggleExpand(item.step_number)}
                          className="w-7 h-7 rounded-lg bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-600"
                        >
                          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </button>
                      </div>
                    </div>

                    {/* Expanded Details */}
                    {isExpanded && (
                      <div className="px-5 pb-5 pt-2 border-t border-slate-100 text-xs text-slate-700 space-y-3.5 bg-slate-50/50">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="p-3 rounded-lg bg-white border border-slate-200 shadow-sm">
                            <p className="text-[10px] font-bold uppercase tracking-wider text-[#1b3bbb] mb-1">
                              Suggested Activity & Learning Method
                            </p>
                            <p className="text-slate-700 leading-relaxed">{item.suggested_activity}</p>
                          </div>
                          <div className="p-3 rounded-lg bg-white border border-slate-200 shadow-sm">
                            <p className="text-[10px] font-bold uppercase tracking-wider text-emerald-700 mb-1">
                              Practical Exercise & Milestone
                            </p>
                            <p className="text-slate-700 leading-relaxed">{item.practical_exercise}</p>
                            <p className="text-[11px] text-[#1b3bbb] font-bold mt-1">
                              Milestone: {item.milestone_project}
                            </p>
                          </div>
                        </div>

                        {/* Verified Resources */}
                        {item.resource_links && item.resource_links.length > 0 && (
                          <div className="flex items-center gap-2 pt-1">
                            <span className="text-[11px] font-bold text-slate-600">
                              Verified Tutorials:
                            </span>
                            <div className="flex flex-wrap gap-2">
                              {item.resource_links.map((res, ri) => (
                                <a
                                  key={ri}
                                  href={res.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-[11px] text-[#1b3bbb] hover:underline flex items-center gap-1 px-2.5 py-0.5 rounded-md bg-blue-50 border border-blue-200 font-semibold"
                                >
                                  <span>{res.title}</span>
                                  <ExternalLink className="w-2.5 h-2.5" />
                                </a>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Personal Learning Notes Box */}
                        <div className="pt-2 border-t border-slate-200">
                          <label className="block text-[11px] font-bold text-slate-700 mb-1">
                            My Study Notes & Code Snippets:
                          </label>
                          <div className="flex gap-2">
                            <input
                              type="text"
                              value={noteVal}
                              onChange={(e) =>
                                setNotesState({ ...notesState, [item.id!]: e.target.value })
                              }
                              placeholder="Add summary notes or git repository links..."
                              className="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#1b3bbb] shadow-sm"
                            />
                            <button
                              onClick={() => handleSaveNotes(item)}
                              disabled={savingItem === item.id}
                              className="px-4 py-1.5 rounded-lg bg-[#1b3bbb] hover:bg-[#152e95] text-white text-xs font-semibold flex items-center gap-1.5 shrink-0 shadow-sm"
                            >
                              <Save className="w-3.5 h-3.5" />
                              <span>{savingItem === item.id ? 'Saving...' : 'Save Note'}</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
