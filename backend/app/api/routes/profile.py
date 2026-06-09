from fastapi import APIRouter, HTTPException
from sqlalchemy import desc

from app.api.deps import DbSession
from app.models import Misconception, SessionRecord, Student
from app.schemas.responses import DashboardResponse, SessionResponse, StudentResponse

router = APIRouter(tags=["profile"])


@router.get("/profile/{student_id}", response_model=StudentResponse)
def profile(student_id: int, db: DbSession) -> StudentResponse:
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


@router.get("/dashboard/{student_id}", response_model=DashboardResponse)
def dashboard(student_id: int, db: DbSession) -> DashboardResponse:
    student = db.get(Student, student_id)
    if not student or not student.profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    misconceptions = db.query(Misconception).filter(Misconception.student_id == student_id).all()
    sessions = (
        db.query(SessionRecord)
        .filter(SessionRecord.student_id == student_id)
        .order_by(desc(SessionRecord.started_at))
        .limit(5)
        .all()
    )
    weak_topics = sorted({item.topic for item in misconceptions})
    bloom_progress = {topic: student.current_bloom_level for topic in weak_topics or ["General Programming"]}
    return DashboardResponse(
        student=student,
        bloom_progress=bloom_progress,
        weak_topics=weak_topics,
        strong_topics=[] if weak_topics else ["Foundations"],
        recent_sessions=sessions,
        learning_streak=len(sessions),
        difficulty_level=student.profile.difficulty_level,
    )


@router.get("/sessions/{student_id}", response_model=list[SessionResponse])
def sessions(student_id: int, db: DbSession) -> list[SessionRecord]:
    return (
        db.query(SessionRecord)
        .filter(SessionRecord.student_id == student_id)
        .order_by(desc(SessionRecord.started_at))
        .limit(20)
        .all()
    )
