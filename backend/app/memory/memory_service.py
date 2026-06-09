from dataclasses import dataclass

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import ChatHistory, LearnerProfile, Misconception, SessionRecord, Student


@dataclass(frozen=True)
class LearningMemory:
    student: Student
    profile: LearnerProfile
    weak_topics: list[str]
    strong_topics: list[str]
    recent_mistakes: list[str]
    recent_sessions: list[SessionRecord]


class MemoryService:
    def fetch(self, db: Session, student_id: int) -> LearningMemory:
        student = db.get(Student, student_id)
        if not student or not student.profile:
            raise ValueError("Student profile not found")
        misconceptions = (
            db.query(Misconception)
            .filter(Misconception.student_id == student_id)
            .order_by(desc(Misconception.created_at))
            .limit(10)
            .all()
        )
        recent_sessions = (
            db.query(SessionRecord)
            .filter(SessionRecord.student_id == student_id)
            .order_by(desc(SessionRecord.started_at))
            .limit(5)
            .all()
        )
        weak_topics = sorted({item.topic for item in misconceptions})
        recent_questions = (
            db.query(ChatHistory)
            .filter(ChatHistory.student_id == student_id)
            .order_by(desc(ChatHistory.timestamp))
            .limit(10)
            .all()
        )
        strong_topics = sorted({item.question[:40] for item in recent_questions if item.model_used.endswith("local") is False})[:5]
        return LearningMemory(
            student=student,
            profile=student.profile,
            weak_topics=weak_topics,
            strong_topics=strong_topics,
            recent_mistakes=[item.misconception for item in misconceptions],
            recent_sessions=recent_sessions,
        )
