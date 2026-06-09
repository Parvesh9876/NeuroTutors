export type Student = {
  id: number;
  name: string;
  email: string;
  learning_level: string;
  current_bloom_level: string;
  confidence_score: number;
  created_at: string;
  profile?: LearnerProfile | null;
};

export type LearnerProfile = {
  preferred_learning_style: string;
  skill_score: number;
  pace_score: number;
  difficulty_level: number;
  preferred_language: string;
  goal: string;
};

export type OnboardingRequest = {
  name: string;
  email: string;
  experience_level: string;
  programming_knowledge: string;
  problem_solving_confidence: number;
  goal: string;
  preferred_language: string;
  preferred_learning_style: string;
};

export type TutorResponse = {
  student_id: number;
  topic: string;
  response: string;
  model_used: string;
  bloom_level: string;
  difficulty_level: number;
  misconception_detected: boolean;
  guiding_questions: string[];
};

export type Dashboard = {
  student: Student;
  bloom_progress: Record<string, string>;
  weak_topics: string[];
  strong_topics: string[];
  recent_sessions: { id: number; topic: string; started_at: string; ended_at?: string | null }[];
  learning_streak: number;
  difficulty_level: number;
};

export type ChatMessage = {
  role: "student" | "tutor";
  content: string;
};
