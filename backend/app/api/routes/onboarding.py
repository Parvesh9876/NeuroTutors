from fastapi import APIRouter, HTTPException

from app.api.deps import DbSession
from app.schemas.requests import OnboardingRequest
from app.schemas.responses import OnboardingResponse
from app.services.profile_service import ProfileService

router = APIRouter(tags=["onboarding"])


@router.post("/onboarding", response_model=OnboardingResponse)
def onboarding(request: OnboardingRequest, db: DbSession) -> OnboardingResponse:
    try:
        student = ProfileService().create_or_update(db, request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Could not create learner profile") from exc
    return OnboardingResponse(
        student=student,
        onboarding_summary=f"{student.name} is profiled as {student.learning_level} with {student.profile.difficulty_level}/5 difficulty.",
    )
