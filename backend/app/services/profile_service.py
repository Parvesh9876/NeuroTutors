from sqlalchemy.orm import Session

from app.models import LearnerProfile, Student
from app.schemas.requests import OnboardingRequest


class ProfileService:
    def create_or_update(self, db: Session, request: OnboardingRequest) -> Student:
        skill_score = self._score_skill(request)
        level = self._level_from_score(skill_score)
        student = db.query(Student).filter(Student.email == request.email).one_or_none()
        if student is None:
            student = Student(name=request.name, email=str(request.email))
            db.add(student)
            db.flush()
        student.name = request.name
        student.learning_level = level
        student.confidence_score = request.problem_solving_confidence / 5
        if student.profile is None:
            student.profile = LearnerProfile(student_id=student.id)
        student.profile.preferred_learning_style = request.preferred_learning_style
        student.profile.skill_score = skill_score
        student.profile.pace_score = min(1.0, max(0.2, request.problem_solving_confidence / 5))
        student.profile.difficulty_level = max(1, min(5, round(skill_score * 5)))
        student.profile.preferred_language = request.preferred_language
        student.profile.goal = request.goal
        db.commit()
        db.refresh(student)
        return student

    def _score_skill(self, request: OnboardingRequest) -> float:
        text = f"{request.experience_level} {request.programming_knowledge}".lower()
        score = request.problem_solving_confidence / 10
        if "none" in text or "beginner" in text:
            score += 0.05
        if "basic" in text:
            score += 0.2
        if "intermediate" in text or "projects" in text:
            score += 0.4
        if "advanced" in text or "competitive" in text or "placement" in text:
            score += 0.55
        return min(1.0, max(0.1, score))

    def _level_from_score(self, score: float) -> str:
        if score < 0.25:
            return "L1 Beginner"
        if score < 0.45:
            return "L2 Basic"
        if score < 0.65:
            return "L3 Intermediate"
        if score < 0.85:
            return "L4 Advanced"
        return "L5 Expert"
