from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.api.routes import analyze, chat, onboarding, profile
from app.config.settings import get_settings
from app.database.session import create_database


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin, "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(onboarding.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(analyze.router, prefix="/api")
    app.include_router(profile.router, prefix="/api")

    @app.on_event("startup")
    def startup() -> None:
        create_database()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": "Invalid request payload", "errors": exc.errors()})

    return app


app = create_app()
