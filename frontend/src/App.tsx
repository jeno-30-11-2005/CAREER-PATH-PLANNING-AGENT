import React, { useState, useEffect } from 'react';
import { Sidebar, NavTab } from './components/Sidebar';
import { Header } from './components/Header';
import { ProfileModal } from './components/ProfileModal';
import { WorkflowModal } from './components/WorkflowModal';
import { DashboardView } from './pages/DashboardView';
import { RecommendationsView } from './pages/RecommendationsView';
import { SkillGapView } from './pages/SkillGapView';
import { RoadmapView } from './pages/RoadmapView';
import { AssistantView } from './pages/AssistantView';
import { VivaPrepView } from './pages/VivaPrepView';
import { api } from './services/api';
import {
  StudentProfile,
  CareerRole,
  RecommendationItem,
  SkillGapResponse,
  LearningRoadmap,
  DashboardOverview,
  WorkflowResult
} from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>('dashboard');
  const [filterPill, setFilterPill] = useState('Overview');

  // Core Data States
  const [student, setStudent] = useState<StudentProfile | null>(null);
  const [roles, setRoles] = useState<CareerRole[]>([]);
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [selectedRoleSlug, setSelectedRoleSlug] = useState<string>('ai-engineer');
  const [gapData, setGapData] = useState<SkillGapResponse | null>(null);
  const [roadmap, setRoadmap] = useState<LearningRoadmap | null>(null);
  const [dashboardOverview, setDashboardOverview] = useState<DashboardOverview | null>(null);

  // Modals & UI States
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [isWorkflowModalOpen, setIsWorkflowModalOpen] = useState(false);
  const [workflowData, setWorkflowData] = useState<WorkflowResult | null>(null);
  const [isApprovingWorkflow, setIsApprovingWorkflow] = useState(false);
  const [assistantInitialQuery, setAssistantInitialQuery] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);

  // Initialize application data
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setIsLoading(true);
    try {
      // 1. Fetch or create student profile
      const profiles = await api.getProfiles();
      let activeProfile: StudentProfile;

      if (profiles.length > 0) {
        activeProfile = profiles[0];
      } else {
        // Create initial default profile
        activeProfile = await api.createProfile({
          name: 'Nadia Rachel',
          education_level: 'Undergraduate',
          degree_specialization: 'BE Artificial Intelligence & Data Science',
          current_year_sem: '3rd Year, Semester 6',
          interests: ['Machine Learning', 'Deep Learning', 'Generative AI', 'Cloud Infrastructure'],
          technical_skills: ['Python', 'SQL', 'Pandas', 'Scikit-Learn'],
          soft_skills: ['Analytical Thinking', 'Team Collaboration'],
          programming_experience: 'Intermediate',
          preferred_career_fields: ['Artificial Intelligence & Data Science'],
          weekly_learning_hours: 12,
          career_goals: 'Aspiring to become an AI Engineer building reliable agentic applications.'
        });
      }
      setStudent(activeProfile);

      // 2. Fetch Knowledge Base Roles
      const fetchedRoles = await api.getCareerRoles();
      setRoles(fetchedRoles);

      // 3. Generate Recommendations
      const recsRes = await api.generateRecommendations(activeProfile.id!);
      setRecommendations(recsRes.recommendations);

      const targetSlug = recsRes.recommendations[0]?.career_role.slug || 'ai-engineer';
      setSelectedRoleSlug(targetSlug);

      // 4. Fetch Skill-Gap for target role
      const gapRes = await api.analyzeSkillGap(activeProfile.id!, targetSlug);
      setGapData(gapRes);

      // 5. Fetch active roadmap
      const activeRoadmap = await api.getStudentRoadmap(activeProfile.id!);
      setRoadmap(activeRoadmap);

      // 6. Fetch dashboard overview
      const overview = await api.getDashboard(activeProfile.id!);
      setDashboardOverview(overview);
    } catch (err) {
      console.error('Initialization error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Re-fetch skill gap whenever selected role changes
  const handleSelectRole = async (slug: string) => {
    setSelectedRoleSlug(slug);
    if (student?.id) {
      try {
        const gap = await api.analyzeSkillGap(student.id, slug);
        setGapData(gap);
      } catch (e) {
        console.error(e);
      }
    }
  };

  // Trigger the Agentic Planning Workflow
  const handleLaunchAgentWorkflow = async (slugOverride?: string) => {
    if (!student?.id) return;
    setIsLoading(true);
    try {
      const targetSlug = slugOverride || selectedRoleSlug;
      const res = await api.runWorkflow(student.id, targetSlug);
      setWorkflowData(res);
      setIsWorkflowModalOpen(true);
    } catch (err: any) {
      alert(`Workflow error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Human Review: Approve proposed plan
  const handleApproveWorkflow = async () => {
    if (!student?.id || !workflowData) return;
    setIsApprovingWorkflow(true);
    try {
      const saved = await api.approveRoadmap(
        student.id,
        workflowData.selected_role.slug,
        workflowData.proposed_roadmap
      );
      setRoadmap(saved);
      setIsWorkflowModalOpen(false);

      // Refresh dashboard
      const overview = await api.getDashboard(student.id);
      setDashboardOverview(overview);
      setActiveTab('roadmap');
    } catch (err: any) {
      alert(`Approval error: ${err.message}`);
    } finally {
      setIsApprovingWorkflow(false);
    }
  };

  // Roadmap step status / note update
  const handleUpdateRoadmapItem = async (itemId: number, status: string, notes: string) => {
    try {
      await api.updateRoadmapItem(itemId, { completion_status: status, learning_notes: notes });
      if (student?.id) {
        const updatedRoadmap = await api.getStudentRoadmap(student.id);
        setRoadmap(updatedRoadmap);
        const overview = await api.getDashboard(student.id);
        setDashboardOverview(overview);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Save profile from modal
  const handleSaveProfile = async (updated: StudentProfile) => {
    if (!student?.id) return;
    try {
      const saved = await api.updateProfile(student.id, updated);
      setStudent(saved);
      setIsProfileModalOpen(false);
      // Refresh recommendations and gap
      const recsRes = await api.generateRecommendations(saved.id!);
      setRecommendations(recsRes.recommendations);
      const gap = await api.analyzeSkillGap(saved.id!, selectedRoleSlug);
      setGapData(gap);
      const overview = await api.getDashboard(saved.id!);
      setDashboardOverview(overview);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0B0B0E] text-slate-100 font-sans">
      {/* Sidebar matching the theme reference */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenSettings={() => setIsProfileModalOpen(true)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        <Header
          student={student}
          onOpenAssistant={(query) => {
            setAssistantInitialQuery(query);
            setActiveTab('assistant');
          }}
          onOpenSettings={() => setIsProfileModalOpen(true)}
          filterPill={filterPill}
          setFilterPill={(pill) => {
            setFilterPill(pill);
            if (pill === 'Roadmap') setActiveTab('roadmap');
            if (pill === 'Skill Matrix') setActiveTab('skillgap');
            if (pill === 'Overview') setActiveTab('dashboard');
          }}
        />

        <main className="flex-1 p-6 sm:p-8 max-w-7xl mx-auto w-full">
          {activeTab === 'dashboard' && (
            <DashboardView
              overview={dashboardOverview}
              student={student}
              recommendations={recommendations}
              onExploreAI={() => handleLaunchAgentWorkflow()}
              onSelectRole={(slug) => {
                handleSelectRole(slug);
                setActiveTab('skillgap');
              }}
              onNavigateToRoadmap={() => setActiveTab('roadmap')}
            />
          )}

          {activeTab === 'roles' && (
            <RecommendationsView
              recommendations={recommendations}
              onSelectRoleForGap={(slug) => {
                handleSelectRole(slug);
                setActiveTab('skillgap');
              }}
              onSelectRoleForRoadmap={(slug) => {
                handleLaunchAgentWorkflow(slug);
              }}
              onRefreshRecommendations={() => student?.id && api.generateRecommendations(student.id).then(r => setRecommendations(r.recommendations))}
              isLoading={isLoading}
            />
          )}

          {activeTab === 'skillgap' && (
            <SkillGapView
              roles={roles}
              selectedRoleSlug={selectedRoleSlug}
              onSelectRole={handleSelectRole}
              gapData={gapData}
              onGenerateRoadmap={(slug) => handleLaunchAgentWorkflow(slug)}
              isLoading={isLoading}
            />
          )}

          {activeTab === 'roadmap' && (
            <RoadmapView
              roadmap={roadmap}
              onUpdateItem={handleUpdateRoadmapItem}
              onTriggerAgentWorkflow={() => handleLaunchAgentWorkflow()}
              isLoading={isLoading}
            />
          )}

          {activeTab === 'assistant' && (
            <AssistantView
              student={student}
              selectedRoleSlug={selectedRoleSlug}
              initialQuery={assistantInitialQuery}
            />
          )}

          {activeTab === 'progress' && (
            <DashboardView
              overview={dashboardOverview}
              student={student}
              recommendations={recommendations}
              onExploreAI={() => handleLaunchAgentWorkflow()}
              onSelectRole={(slug) => {
                handleSelectRole(slug);
                setActiveTab('skillgap');
              }}
              onNavigateToRoadmap={() => setActiveTab('roadmap')}
            />
          )}

          {activeTab === 'viva' && <VivaPrepView />}
        </main>
      </div>

      {/* Profile Settings Modal */}
      <ProfileModal
        isOpen={isProfileModalOpen}
        onClose={() => setIsProfileModalOpen(false)}
        profile={student}
        onSave={handleSaveProfile}
      />

      {/* Agentic Workflow Human Approval Modal */}
      <WorkflowModal
        isOpen={isWorkflowModalOpen}
        onClose={() => setIsWorkflowModalOpen(false)}
        workflowData={workflowData}
        onApprove={handleApproveWorkflow}
        isApproving={isApprovingWorkflow}
      />
    </div>
  );
};

export default App;
