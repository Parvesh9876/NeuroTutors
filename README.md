# NeuroTutor

NeuroTutor is a production-minded MVP for an adaptive AI learning platform. It is not a direct-answer chatbot: the backend profiles learners, guards against answer-bypass prompts, routes between fast and reasoning models, retrieves learning memory, detects misconceptions, applies Bloom's taxonomy, and responds with Socratic tutoring.

## Architecture

Student -> Next.js frontend -> FastAPI -> LangGraph agent orchestrator -> guard -> route -> learner memory -> Socratic tutor -> evaluator -> database update.

## Stack

- Frontend: Next.js 15, TypeScript, TailwindCSS, Shadcn-style local UI primitives, Zustand, Axios, Monaco Editor
- Backend: FastAPI, Python 3.12, SQLAlchemy, Pydantic, SQLite
- AI: LangGraph, LangChain, Groq Llama 3 for fast routing, GPT-4o for reasoning routing

The app runs without API keys by using a local tutoring fallback. Add keys to enable live model calls.

## Setup

1. Backend

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

If Python 3.12 is not installed, use your available Python launcher version for local development. Docker uses Python 3.12.

2. Frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open `http://localhost:3000`. The API docs are at `http://localhost:8000/docs`.

## Environment

Backend `.env`:

```env
OPENAI_API_KEY=
GROQ_API_KEY=
DATABASE_URL=sqlite:///./neurotutor.db
JWT_SECRET=replace-me-with-a-long-secret
FRONTEND_ORIGIN=http://localhost:3000
```

Frontend `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

## Docker

```powershell
Copy-Item backend\.env.example backend\.env
docker compose up --build
```

## Tests

```powershell
cd backend
pytest
```

```powershell
cd frontend
npm run typecheck
npm run build
```

## API

- `POST /api/onboarding` creates or updates a learner profile from assessment answers.
- `POST /api/chat` runs the adaptive Socratic agent pipeline.
- `POST /api/analyze` analyzes Python or Java code from the Monaco workspace.
- `GET /api/profile/{id}` returns the learner profile.
- `GET /api/dashboard/{id}` returns progress, weak topics, sessions, and difficulty.
- `GET /api/sessions/{id}` returns recent learning sessions.

## Notes

- Secrets are never hardcoded.
- Requests and responses use strict Pydantic schemas.
- The guard node redirects prompt injection attempts into a learning-oriented question.
- The model router sends low-complexity requests to Groq Llama 3 and higher-complexity requests to GPT-4o when keys are configured.
