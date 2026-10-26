import React from 'react';
import { Search, Bell, Settings, Sparkles, ChevronRight } from 'lucide-react';
import { StudentProfile } from '../types';

interface HeaderProps {
  student: StudentProfile | null;
  onOpenAssistant: (initialQuery?: string) => void;
  onOpenSettings: () => void;
  filterPill: string;
  setFilterPill: (pill: string) => void;
}

export const Header: React.FC<HeaderProps> = ({
  student,
  onOpenAssistant,
  onOpenSettings,
  filterPill,
  setFilterPill
}) => {
  const [searchQuery, setSearchQuery] = React.useState('');

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onOpenAssistant(searchQuery.trim());
      setSearchQuery('');
    }
  };

  const displayName = student?.name || 'Nadia Rachel';
  const displayEmail = student ? `${student.name.toLowerCase().replace(/\s+/g, '_')}@college.edu` : 'nadiarachel@college.edu';

  return (
    <div className="bg-white border-b border-slate-200">
      {/* Notice Banner matching Rubick's blue top announcement */}
      <div className="bg-[#1b3bbb] text-white px-8 py-2 text-xs flex items-center justify-between font-medium">
        <div className="flex items-center gap-2">
          <span className="bg-white/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">
            Academic Project
          </span>
          <span>Intelligent Career Path Planning Agent • BE AI & Data Science</span>
        </div>
        <span className="text-[11px] text-blue-100 hidden md:inline">
          Deterministic Matching • 5-Phase Roadmaps • Gemini AI Assistant
        </span>
      </div>

      {/* Main Top Header */}
      <header className="px-8 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Breadcrumb & Welcome Title */}
        <div>
          <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
            <span>Application</span>
            <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-800 font-semibold">Dashboard</span>
          </div>
          <h1 className="text-xl font-bold text-slate-800 mt-1 tracking-tight">
            Welcome, <span className="text-[#1b3bbb]">{displayName}</span>
          </h1>

          {/* Filter Pills matching Rubick style */}
          <div className="flex items-center gap-2 mt-3">
            {['Overview', 'Roadmap', 'Skill Matrix'].map((pill) => (
              <button
                key={pill}
                onClick={() => setFilterPill(pill)}
                className={`px-3.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                  filterPill === pill
                    ? 'bg-[#1b3bbb] text-white shadow-sm'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200 border border-slate-200'
                }`}
              >
                {pill}
              </button>
            ))}
          </div>
        </div>

        {/* Right Search, Notification, and User Avatar */}
        <div className="flex items-center gap-3">
          {/* Search bar matching Rubick */}
          <form onSubmit={handleSearchSubmit} className="relative">
            <div className="flex items-center bg-slate-100 border border-slate-200 rounded-xl px-3.5 py-2 w-64 focus-within:bg-white focus-within:border-[#1b3bbb] focus-within:ring-2 focus-within:ring-blue-100 transition-all">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search career, skills, roadmaps..."
                className="bg-transparent text-xs text-slate-700 placeholder-slate-400 focus:outline-none w-full"
              />
              <Search className="w-4 h-4 text-slate-400 shrink-0 ml-1.5 cursor-pointer" />
            </div>
          </form>

          {/* Notification Bell */}
          <button
            onClick={() => alert("Notification: Your personalized career roadmap is up to date!")}
            className="w-9 h-9 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center transition-all relative border border-slate-200"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-[#1b3bbb]"></span>
          </button>

          {/* Settings Button */}
          <button
            onClick={onOpenSettings}
            className="w-9 h-9 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center transition-all border border-slate-200"
          >
            <Settings className="w-4 h-4" />
          </button>

          {/* User Profile Avatar matching Rubick top right */}
          <div
            onClick={onOpenSettings}
            className="flex items-center gap-2.5 pl-2 pr-3 py-1 rounded-xl hover:bg-slate-100 transition-all cursor-pointer border border-transparent hover:border-slate-200"
          >
            <div className="w-8 h-8 rounded-full bg-[#1b3bbb] text-white flex items-center justify-center text-xs font-bold shadow-sm">
              {displayName[0]}
            </div>
            <div className="text-left hidden sm:block">
              <p className="text-xs font-bold text-slate-800 leading-tight">{displayName}</p>
              <p className="text-[10px] text-slate-500 leading-tight">{displayEmail}</p>
            </div>
          </div>
        </div>
      </header>
    </div>
  );
};
