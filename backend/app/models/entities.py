from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    learning_level: Mapped[str] = mapped_column(String(20), default="L1 Beginner")
    current_bloom_level: Mapped[str] = mapped_column(String(20), default="Remember")
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profile: Mapped["LearnerProfile"] = relationship(back_populates="student", uselist=False, cascade="all, delete-orphan")
    misconceptions: Mapped[list["Misconception"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    sessions: Mapped[list["SessionRecord"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    chat_history: Mapped[list["ChatHistory"]] = relationship(back_populates="student", cascade="all, delete-orphan")


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True, nullable=False)
    preferred_learning_style: Mapped[str] = mapped_column(String(60), default="guided examples")
    skill_score: Mapped[float] = mapped_column(Float, default=0.2)
    pace_score: Mapped[float] = mapped_column(Float, default=0.5)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)
    preferred_language: Mapped[str] = mapped_column(String(40), default="Python")
    goal: Mapped[str] = mapped_column(String(120), default="general learning")

    student: Mapped[Student] = relationship(back_populates="profile")


class Misconception(Base):
    __tablename__ = "misconceptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    topic: Mapped[str] = mapped_column(String(120), nullable=False)
    misconception: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student: Mapped[Student] = relationship(back_populates="misconceptions")


class SessionRecord(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    topic: Mapped[str] = mapped_column(String(120), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    student: Mapped[Student] = relationship(back_populates="sessions")


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[str] = mapped_column(String(80), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student: Mapped[Student] = relationship(back_populates="chat_history")
