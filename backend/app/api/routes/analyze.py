from fastapi import APIRouter, HTTPException

from app.api.deps import DbSession
from app.models import ChatHistory, Student
from app.schemas.requests import AnalyzeCodeRequest
from app.schemas.responses import CodeAnalysisResponse
from app.services.code_analysis_service import CodeAnalysisService

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=CodeAnalysisResponse)
def analyze_code(request: AnalyzeCodeRequest, db: DbSession) -> CodeAnalysisResponse:
    if db.get(Student, request.student_id) is None:
        raise HTTPException(status_code=404, detail="Student profile not found")
    guidance, findings, detected = CodeAnalysisService().analyze(request.code, request.language, request.topic)
    db.add(ChatHistory(student_id=request.student_id, question=f"Analyze {request.language} code", response=guidance, model_used="static-analyzer"))
    db.commit()
    return CodeAnalysisResponse(
        student_id=request.student_id,
        language=request.language,
        guidance=guidance,
        findings=findings,
        misconception_detected=detected,
    )
