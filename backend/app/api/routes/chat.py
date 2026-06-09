from fastapi import APIRouter, HTTPException

from app.agents.orchestrator import AgentOrchestrator
from app.api.deps import AppSettings, DbSession
from app.schemas.requests import ChatRequest
from app.schemas.responses import TutorResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=TutorResponse)
async def chat(request: ChatRequest, db: DbSession, settings: AppSettings) -> TutorResponse:
    try:
        state = await AgentOrchestrator(db, settings).run(request.student_id, request.question, request.topic)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Tutor engine is temporarily unavailable") from exc
    return TutorResponse(
        student_id=request.student_id,
        topic=request.topic,
        response=state["response"],
        model_used=state["model_used"],
        bloom_level=state.get("bloom_level", "Remember"),
        difficulty_level=state.get("difficulty_level", 1),
        misconception_detected=state.get("misconception_detected", False),
        guiding_questions=state.get("guiding_questions", []),
    )
