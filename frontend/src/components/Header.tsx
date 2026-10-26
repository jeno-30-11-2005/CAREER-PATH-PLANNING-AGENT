import React from 'react';
import { Search, Bell, Settings, Sparkles } from 'lucide-react';
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
    <header className="px-8 pt-8 pb-4 flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-white/5 bg-[#0B0B0E]">
      {/* Welcome Greeting and Filter Pills */}
      <div>
        <div className="flex items-baseline gap-2">
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Welcome, <span className="text-[#E0AAFF]">{displayName.split(' ')[0]}</span>
          </h1>
        </div>
        <p className="text-xs text-slate-400 mt-0.5">
          Here's your career preparation & readiness overview
        </p>

        {/* Filter Pills matching the reference image (Market, Wallet, Tools) */}
        <div className="flex items-center gap-2 mt-4">
          {['Overview', 'Roadmap', 'Skill Matrix'].map((pill) => (
            <button
              key={pill}
              onClick={() => setFilterPill(pill)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
                filterPill === pill
                  ? 'bg-[#1C1C29] text-white border border-purple-500/40 shadow-glow-subtle'
                  : 'bg-[#13131A] text-slate-400 hover:text-slate-200 border border-white/5'
              }`}
            >
              {pill}
            </button>
          ))}
        </div>
      </div>

      {/* Right Controls: Search Pill, Bell, Settings, User Profile */}
      <div className="flex items-center gap-3">
        {/* "Ask career.ai anything" Pill Bar */}
        <form onSubmit={handleSearchSubmit} className="relative">
          <div className="flex items-center bg-[#13131A] border border-white/10 hover:border-purple-500/40 focus-within:border-purple-500/60 rounded-full px-4 py-2 transition-all w-64 md:w-72 shadow-inner">
            <Sparkles className="w-4 h-4 text-[#C77DFF] mr-2 shrink-0 animate-pulse" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Ask career.ai anything..."
              className="bg-transparent text-xs text-slate-200 placeholder-slate-500 focus:outline-none w-full"
            />
          </div>
        </form>

        {/* Notification Bell */}
        <button
          onClick={() => alert("Notification: Your personalized career roadmap is up to date!")}
          className="w-10 h-10 rounded-full bg-[#13131A] border border-white/10 flex items-center justify-center text-slate-300 hover:text-white hover:border-purple-500/40 transition-all relative"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-[#C77DFF] ring-2 ring-[#0B0B0E]"></span>
        </button>

        {/* Settings Button */}
        <button
          onClick={onOpenSettings}
          className="w-10 h-10 rounded-full bg-[#13131A] border border-white/10 flex items-center justify-center text-slate-300 hover:text-white hover:border-purple-500/40 transition-all"
        >
          <Settings className="w-4 h-4" />
        </button>

        {/* User Profile Chip matching the reference screenshot */}
        <div
          onClick={onOpenSettings}
          className="flex items-center gap-3 pl-2 pr-4 py-1.5 rounded-full bg-[#13131A] border border-white/10 hover:border-purple-500/40 transition-all cursor-pointer"
        >
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#9D4EDD] to-[#E0AAFF] flex items-center justify-center text-xs font-bold text-white shadow-sm">
            {displayName[0]}
          </div>
          <div className="text-left hidden sm:block">
            <p className="text-xs font-semibold text-white leading-tight">{displayName}</p>
            <p className="text-[10px] text-slate-400 leading-tight">{displayEmail}</p>
          </div>
        </div>
      </div>
    </header>
  );
};
