from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OnboardingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    experience_level: str = Field(min_length=1, max_length=80)
    programming_knowledge: str = Field(min_length=1, max_length=200)
    problem_solving_confidence: int = Field(ge=1, le=5)
    goal: str = Field(min_length=1, max_length=120)
    preferred_language: str = Field(min_length=1, max_length=40)
    preferred_learning_style: str = Field(default="guided examples", max_length=60)


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    student_id: int = Field(gt=0)
    question: str = Field(min_length=1, max_length=4000)
    topic: str = Field(default="General Programming", min_length=1, max_length=120)


class AnalyzeCodeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    student_id: int = Field(gt=0)
    code: str = Field(min_length=1, max_length=12000)
    language: str = Field(pattern="^(python|java)$")
    topic: str = Field(default="Coding Practice", min_length=1, max_length=120)
