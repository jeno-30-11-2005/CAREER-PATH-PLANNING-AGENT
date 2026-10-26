import React from 'react';
import {
  LayoutDashboard,
  Compass,
  GitMerge,
  MapPin,
  MessageSquare,
  TrendingUp,
  GraduationCap,
  Settings,
  HelpCircle,
  Sparkles,
  ChevronRight
} from 'lucide-react';

export type NavTab = 'dashboard' | 'roles' | 'skillgap' | 'roadmap' | 'assistant' | 'progress' | 'viva';

interface SidebarProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
  onOpenSettings: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, onOpenSettings }) => {
  const navItems = [
    { id: 'dashboard' as NavTab, label: 'Dashboard', icon: LayoutDashboard },
    { id: 'roles' as NavTab, label: 'Explore Roles', icon: Compass },
    { id: 'skillgap' as NavTab, label: 'Skill Gap', icon: GitMerge },
    { id: 'roadmap' as NavTab, label: 'Roadmap', icon: MapPin },
    { id: 'assistant' as NavTab, label: 'AI Assistant', icon: MessageSquare },
    { id: 'progress' as NavTab, label: 'Progress', icon: TrendingUp },
    { id: 'viva' as NavTab, label: 'Viva Hub', icon: GraduationCap },
  ];

  return (
    <aside className="w-64 bg-[#1b3bbb] text-white flex flex-col justify-between p-5 min-h-screen shrink-0 shadow-lg select-none">
      <div>
        {/* Brand Logo matching the Rubick reference */}
        <div className="flex items-center gap-3 px-3 py-3 mb-6">
          <div className="w-9 h-9 rounded-xl bg-white text-[#1b3bbb] flex items-center justify-center font-black text-lg shadow-sm">
            <Sparkles className="w-5 h-5 text-[#1b3bbb]" />
          </div>
          <div>
            <span className="font-extrabold text-xl tracking-tight text-white flex items-center gap-1">
              Rubick<span className="text-blue-200 text-sm font-semibold">AI</span>
            </span>
            <p className="text-[11px] text-blue-100/70 font-medium leading-none">Career Planning Agent</p>
          </div>
        </div>

        {/* Section title */}
        <p className="px-3 text-[10px] uppercase font-bold tracking-wider text-blue-200/60 mb-2">
          Core Modules
        </p>

        {/* Navigation list */}
        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-150 ${
                  isActive
                    ? 'bg-white text-[#1b3bbb] shadow-md'
                    : 'text-white/80 hover:text-white hover:bg-white/10'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-[#1b3bbb]' : 'text-blue-200'}`} />
                  <span>{item.label}</span>
                </div>
                {isActive && <ChevronRight className="w-3.5 h-3.5 text-[#1b3bbb]" />}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer controls matching reference */}
      <div className="pt-4 border-t border-white/15 space-y-1">
        <button
          onClick={onOpenSettings}
          className="w-full flex items-center gap-3 px-3.5 py-2 rounded-xl text-xs font-medium text-white/80 hover:text-white hover:bg-white/10 transition-all"
        >
          <Settings className="w-4 h-4 text-blue-200" />
          <span>Edit Profile</span>
        </button>
        <button
          onClick={() => setActiveTab('viva')}
          className="w-full flex items-center gap-3 px-3.5 py-2 rounded-xl text-xs font-medium text-white/80 hover:text-white hover:bg-white/10 transition-all"
        >
          <HelpCircle className="w-4 h-4 text-blue-200" />
          <span>Viva Questions</span>
        </button>
      </div>
    </aside>
  );
};
