import {
  StudentProfile,
  CareerRole,
  RecommendationItem,
  SkillGapResponse,
  LearningRoadmap,
  RoadmapItem,
  DashboardOverview,
  WorkflowResult
} from '../types';

const API_BASE = '/api/v1';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorData.detail || `Request failed with status ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Health
  checkHealth: async () => {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<{ status: string; service: string; llm_provider: string }>(res);
  },

  // Student Profiles
  getProfiles: async (): Promise<StudentProfile[]> => {
    const res = await fetch(`${API_BASE}/profiles/`);
    return handleResponse<StudentProfile[]>(res);
  },

  getProfile: async (id: number): Promise<StudentProfile> => {
    const res = await fetch(`${API_BASE}/profiles/${id}`);
    return handleResponse<StudentProfile>(res);
  },

  createProfile: async (profile: Omit<StudentProfile, 'id'>): Promise<StudentProfile> => {
    const res = await fetch(`${API_BASE}/profiles/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile)
    });
    return handleResponse<StudentProfile>(res);
  },

  updateProfile: async (id: number, profile: Partial<StudentProfile>): Promise<StudentProfile> => {
    const res = await fetch(`${API_BASE}/profiles/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile)
    });
    return handleResponse<StudentProfile>(res);
  },

  // Career Roles
  getCareerRoles: async (): Promise<CareerRole[]> => {
    const res = await fetch(`${API_BASE}/careers/`);
    return handleResponse<CareerRole[]>(res);
  },

  getCareerRole: async (slug: string): Promise<CareerRole> => {
    const res = await fetch(`${API_BASE}/careers/${slug}`);
    return handleResponse<CareerRole>(res);
  },

  // Recommendations
  generateRecommendations: async (profileId: number): Promise<{ recommendations: RecommendationItem[] }> => {
    const res = await fetch(`${API_BASE}/recommendations/generate/${profileId}`, {
      method: 'POST'
    });
    return handleResponse<{ recommendations: RecommendationItem[] }>(res);
  },

  // Skill Gap Analysis
  analyzeSkillGap: async (profileId: number, roleSlug: string): Promise<SkillGapResponse> => {
    const res = await fetch(`${API_BASE}/skill-gap/${profileId}/${roleSlug}`);
    return handleResponse<SkillGapResponse>(res);
  },

  // Roadmaps
  proposeRoadmap: async (profileId: number, roleSlug: string): Promise<{ proposal: LearningRoadmap }> => {
    const res = await fetch(`${API_BASE}/roadmaps/propose/${profileId}/${roleSlug}`, {
      method: 'POST'
    });
    return handleResponse<{ proposal: LearningRoadmap }>(res);
  },

  approveRoadmap: async (profileId: number, roleSlug: string, proposal: LearningRoadmap): Promise<LearningRoadmap> => {
    const res = await fetch(`${API_BASE}/roadmaps/approve/${profileId}/${roleSlug}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(proposal)
    });
    return handleResponse<LearningRoadmap>(res);
  },

  getStudentRoadmap: async (profileId: number): Promise<LearningRoadmap | null> => {
    const res = await fetch(`${API_BASE}/roadmaps/student/${profileId}`);
    return handleResponse<LearningRoadmap | null>(res);
  },

  updateRoadmapItem: async (itemId: number, update: { completion_status?: string; learning_notes?: string }): Promise<RoadmapItem> => {
    const res = await fetch(`${API_BASE}/roadmaps/items/${itemId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(update)
    });
    return handleResponse<RoadmapItem>(res);
  },

  // Dashboard Overview
  getDashboard: async (profileId: number): Promise<DashboardOverview> => {
    const res = await fetch(`${API_BASE}/dashboard/${profileId}`);
    return handleResponse<DashboardOverview>(res);
  },

  // AI Assistant Chat
  chatWithAssistant: async (message: string, studentProfileId?: number, roleSlug?: string, sessionId?: number) => {
    const res = await fetch(`${API_BASE}/assistant/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        student_profile_id: studentProfileId,
        career_role_slug: roleSlug,
        session_id: sessionId
      })
    });
    return handleResponse<{ session_id: number; role: string; content: string; is_fallback: boolean; sources: string[] }>(res);
  },

  // Agentic Workflow Orchestration
  runWorkflow: async (studentProfileId: number, selectedRoleSlug?: string): Promise<WorkflowResult> => {
    const res = await fetch(`${API_BASE}/workflow/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_profile_id: studentProfileId,
        selected_role_slug: selectedRoleSlug
      })
    });
    return handleResponse<WorkflowResult>(res);
  }
};
