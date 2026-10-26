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
  Sparkles
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
    { id: 'viva' as NavTab, label: 'Viva & Defense', icon: GraduationCap },
  ];

  return (
    <aside className="w-64 bg-[#0F0F14] border-r border-white/5 flex flex-col justify-between p-5 min-h-screen">
      <div>
        {/* Brand Logo matching the reference theme */}
        <div className="flex items-center gap-3 px-2 py-3 mb-8">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#9D4EDD] to-[#C77DFF] flex items-center justify-center shadow-glow-violet">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="font-bold text-lg tracking-tight text-white flex items-center gap-1">
              Career<span className="text-[#C77DFF]">AI</span>
            </span>
            <p className="text-[11px] text-slate-400 font-medium">Planning Agent</p>
          </div>
        </div>

        {/* Navigation list */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'neon-pill-active text-white font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-[#E0AAFF]' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer controls matching reference */}
      <div className="pt-6 border-t border-white/5 space-y-1">
        <button
          onClick={onOpenSettings}
          className="w-full flex items-center gap-3.5 px-4 py-2.5 rounded-2xl text-sm font-medium text-slate-400 hover:text-slate-200 hover:bg-white/5 transition-all"
        >
          <Settings className="w-4 h-4 text-slate-400" />
          <span>Edit Profile</span>
        </button>
        <button
          onClick={() => setActiveTab('viva')}
          className="w-full flex items-center gap-3.5 px-4 py-2.5 rounded-2xl text-sm font-medium text-slate-400 hover:text-slate-200 hover:bg-white/5 transition-all"
        >
          <HelpCircle className="w-4 h-4 text-slate-400" />
          <span>Viva Guide</span>
        </button>
      </div>
    </aside>
  );
};
