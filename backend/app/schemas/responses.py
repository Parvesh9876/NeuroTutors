from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LearnerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    preferred_learning_style: str
    skill_score: float
    pace_score: float
    difficulty_level: int
    preferred_language: str
    goal: str


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    learning_level: str
    current_bloom_level: str
    confidence_score: float
    created_at: datetime
    profile: LearnerProfileResponse | None = None


class OnboardingResponse(BaseModel):
    student: StudentResponse
    onboarding_summary: str


class TutorResponse(BaseModel):
    student_id: int
    topic: str
    response: str
    model_used: str
    bloom_level: str
    difficulty_level: int
    misconception_detected: bool
    guiding_questions: list[str]


class CodeAnalysisResponse(BaseModel):
    student_id: int
    language: str
    guidance: str
    findings: list[str]
    misconception_detected: bool


class MisconceptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    topic: str
    misconception: str
    severity: int
    created_at: datetime


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    started_at: datetime
    ended_at: datetime | None


class DashboardResponse(BaseModel):
    student: StudentResponse
    bloom_progress: dict[str, str]
    weak_topics: list[str]
    strong_topics: list[str]
    recent_sessions: list[SessionResponse]
    learning_streak: int
    difficulty_level: int
