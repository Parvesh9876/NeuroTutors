from typing import TypedDict

from app.memory.memory_service import LearningMemory


class TutorState(TypedDict, total=False):
    student_id: int
    question: str
    topic: str
    guarded: bool
    redirect: str
    memory: LearningMemory
    complexity: int
    provider: str
    model: str
    misconception_detected: bool
    misconception: str
    severity: int
    response: str
    model_used: str
    guiding_questions: list[str]
    bloom_level: str
    difficulty_level: int
