export interface StudentProfile {
  id?: number;
  name: string;
  education_level: string;
  degree_specialization: string;
  current_year_sem: string;
  interests: string[];
  technical_skills: string[];
  soft_skills: string[];
  programming_experience: string;
  preferred_career_fields: string[];
  weekly_learning_hours: number;
  career_goals?: string;
  created_at?: string;
  updated_at?: string;
}

export interface CareerRole {
  id: number;
  slug: string;
  title: string;
  category: string;
  description: string;
  required_skills: string[];
  recommended_skills: string[];
  tools_technologies: string[];
  example_projects: string[];
  learning_sequence: string[];
  prerequisites: string[];
}

export interface RecommendationItem {
  career_role: CareerRole;
  match_score: number;
  matching_interests: string[];
  matching_skills: string[];
  missing_skills: string[];
  explanation: string;
  suggested_next_steps: string[];
}

export interface SkillGapItem {
  skill: string;
  category: string;
  status: 'confirmed' | 'partial' | 'unreported';
  priority: number;
  prerequisites: string[];
}

export interface SkillGapResponse {
  career_role_title: string;
  career_role_slug: string;
  total_required_skills: number;
  confirmed_skills: string[];
  partially_developed_skills: string[];
  not_yet_reported_skills: string[];
  detailed_skills: SkillGapItem[];
  recommended_learning_order: string[];
  disclaimer: string;
}

export interface RoadmapResource {
  title: string;
  url: string;
}

export interface RoadmapItem {
  id?: number;
  phase: string;
  step_number: number;
  skill_topic: string;
  why_it_matters: string;
  prerequisites: string[];
  suggested_activity: string;
  estimated_effort_hours: number;
  practical_exercise: string;
  milestone_project: string;
  completion_status: 'not_started' | 'in_progress' | 'completed';
  resource_links: RoadmapResource[];
  learning_notes?: string;
}

export interface LearningRoadmap {
  id?: number;
  student_profile_id: number;
  career_role_id: number;
  title: string;
  target_role: string;
  weekly_hours: number;
  total_estimated_weeks: number;
  is_approved: boolean;
  generation_method: string;
  items: RoadmapItem[];
}

export interface DashboardOverview {
  student_profile: StudentProfile | null;
  profile_completeness_percentage: number;
  recommended_roles_count: number;
  active_roadmap: LearningRoadmap | null;
  completed_steps_count: number;
  total_steps_count: number;
  overall_progress_percentage: number;
  next_skills_to_learn: string[];
}

export interface WorkflowResult {
  status: string;
  workflow_log: string[];
  profile_analysis: any;
  top_recommendations: RecommendationItem[];
  selected_role: {
    id: number;
    slug: string;
    title: string;
    category: string;
  };
  skill_gap_summary: SkillGapResponse;
  proposed_roadmap: LearningRoadmap;
  quality_review: {
    passed: boolean;
    checks_run: string[];
    issues_addressed: string[];
  };
  requires_human_approval: boolean;
  instruction: string;
}
