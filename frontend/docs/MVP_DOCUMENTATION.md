# NeuroTutor MVP Documentation

This document explains the current NeuroTutor MVP feature by feature, then walks through how each request moves through the frontend, backend, AI orchestration layer, and SQLite database.

## 1. Product Summary

NeuroTutor is an adaptive AI learning platform. It is intentionally not designed as a normal chatbot that gives final answers immediately. Its teaching behavior is built around:

- learner profiling
- Socratic guidance
- adaptive difficulty
- Bloom's taxonomy tracking
- anti-jailbreak protection
- misconception detection
- learning memory
- live code analysis
- progress dashboard
- hybrid model routing

The MVP can run without API keys. When `OPENAI_API_KEY` or `GROQ_API_KEY` are missing, the backend returns a local fallback tutoring response so the product remains usable during local development.

## 2. Technology Stack

Frontend:

- Next.js 15
- TypeScript
- TailwindCSS
- Zustand
- Axios
- Monaco Editor
- Local Shadcn-style UI primitives

Backend:

- FastAPI
- Python 3.12
- SQLAlchemy
- Pydantic
- SQLite

AI and agent orchestration:

- LangGraph
- LangChain
- Groq Llama 3 route for fast/simple questions
- GPT-4o route for more complex/reasoning questions
- Local fallback response when keys are unavailable

## 3. High-Level Architecture

```text
Student
  |
  v
Next.js Frontend
  |
  v
FastAPI Backend
  |
  v
Agent Orchestrator
  |
  v
Guard Node
  |
  v
Route Node
  |
  v
Memory Node
  |
  v
Misconception Detector
  |
  v
Socratic Tutor
  |
  v
Adaptive Evaluator
  |
  v
Database Update
  |
  v
Response to Frontend
```

The actual LangGraph node order in code is:

```text
guard_node -> memory_node -> route_node -> detect_node -> tutor_node -> persist_node -> END
```

If the guard blocks the input, the graph skips tutoring and goes directly to persistence with an educational redirect.

## 4. Folder Structure

```text
backend/
  app/
    agents/       LangGraph state and orchestration
    api/          FastAPI dependencies and routes
    config/       environment settings
    database/     SQLAlchemy engine/session creation
    evaluator/    misconception and adaptive difficulty logic
    guard/        prompt injection detection
    memory/       learner memory retrieval
    models/       SQLAlchemy database models
    prompts/      LLM system prompts
    router/       model complexity routing
    schemas/      Pydantic request/response models
    services/     reusable business services
    tutor/        Socratic prompt and guiding question logic
    main.py       FastAPI app factory
  tests/
  requirements.txt

frontend/
  app/            Next.js app routes and global styles
  components/     UI components grouped by feature
  hooks/          custom React hooks
  services/       Axios API client
  store/          Zustand state store
  types/          TypeScript domain types
  utils/          small frontend utilities
```

## 5. Environment Configuration

Backend file: `backend/.env`

```env
OPENAI_API_KEY=
GROQ_API_KEY=
DATABASE_URL=sqlite:///./neurotutor.db
JWT_SECRET=change-this-to-a-long-random-secret
APP_ENV=local
FRONTEND_ORIGIN=http://localhost:3000
```

Frontend file: `frontend/.env.local`

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

Important behavior:

- `DATABASE_URL=sqlite:///./neurotutor.db` creates a SQLite file in `backend/neurotutor.db`.
- Empty model API keys are allowed in local development.
- The backend CORS origin is configured through `FRONTEND_ORIGIN`.

## 6. Database Design

Database file:

```text
backend/neurotutor.db
```

SQLAlchemy creates tables on backend startup through `create_database()`.

### students

Stores the main learner identity and learning state.

Fields:

- `id`: primary key
- `name`: student name
- `email`: unique email
- `learning_level`: L1 to L5 classification
- `current_bloom_level`: current Bloom taxonomy level
- `confidence_score`: normalized confidence score
- `created_at`: creation timestamp

Relationships:

- one `learner_profiles` row
- many `misconceptions`
- many `sessions`
- many `chat_history` rows

### learner_profiles

Stores adaptive learning preferences and skill estimates.

Fields:

- `id`
- `student_id`
- `preferred_learning_style`
- `skill_score`
- `pace_score`
- `difficulty_level`
- `preferred_language`
- `goal`

### misconceptions

Stores detected misunderstandings.

Fields:

- `id`
- `student_id`
- `topic`
- `misconception`
- `severity`
- `created_at`

### sessions

Stores learning session records.

Fields:

- `id`
- `student_id`
- `topic`
- `started_at`
- `ended_at`

Current MVP behavior creates a session row for each tutor interaction.

### chat_history

Stores each tutor or code analysis exchange.

Fields:

- `id`
- `student_id`
- `question`
- `response`
- `model_used`
- `timestamp`

## 7. Frontend Features

### 7.1 Onboarding Form

File:

```text
frontend/components/Profile/OnboardingForm.tsx
```

Purpose:

- collects learner details
- sends them to `POST /api/onboarding`
- stores the returned student in Zustand
- adds an onboarding summary message to the tutor chat

Inputs:

- name
- email
- experience level
- programming knowledge
- confidence score
- learning goal
- preferred language
- preferred learning style

Behind the scenes:

```text
User submits form
  -> onboard() in frontend/services/api.ts
  -> POST /api/onboarding
  -> ProfileService.create_or_update()
  -> students + learner_profiles updated
  -> response saved in Zustand
```

### 7.2 Chat Tutor

File:

```text
frontend/components/Chat/ChatTutor.tsx
```

Purpose:

- provides the student-facing tutor conversation
- prevents sending messages before a profile exists
- sends the active topic and student question to the backend
- displays tutor response, guiding questions, and selected model
- refreshes dashboard data after each tutor response

Behind the scenes:

```text
Student asks question
  -> sendTutorMessage()
  -> POST /api/chat
  -> LangGraph tutor pipeline
  -> response added to chat
  -> GET /api/dashboard/{student_id}
  -> progress panel refreshes
```

### 7.3 Live Coding Workspace

File:

```text
frontend/components/Editor/CodeWorkspace.tsx
```

Purpose:

- provides Monaco Editor
- supports Python and Java modes
- stores code in Zustand
- sends code to backend after a 2-second debounce
- displays tutor-like code analysis

Behind the scenes:

```text
Student edits code
  -> Zustand code state updates
  -> useDebouncedEffect waits 2 seconds
  -> analyzeCode()
  -> POST /api/analyze
  -> CodeAnalysisService.analyze()
  -> guidance shown below editor
```

Current MVP code checks:

- Python syntax through `ast.parse`
- Java class wrapper presence
- Java brace balance
- simple infinite-loop signal
- misconception rules against submitted code text

### 7.4 Progress Panel

File:

```text
frontend/components/Dashboard/ProgressPanel.tsx
```

Purpose:

- shows Bloom level
- shows current difficulty
- shows learning streak
- shows skill score progress
- shows weak topics

Data source:

- initially uses current student/profile from Zustand
- after chat, uses `GET /api/dashboard/{student_id}`

### 7.5 Global State

File:

```text
frontend/store/useLearningStore.ts
```

Zustand stores:

- current student
- dashboard
- chat messages
- active topic
- active coding language
- current code editor content

This lets chat, editor, onboarding, and dashboard share state without prop drilling.

## 8. Backend API Documentation

All API routes are mounted under `/api`.

### POST /api/onboarding

File:

```text
backend/app/api/routes/onboarding.py
```

Request schema:

```text
OnboardingRequest
```

Creates or updates:

- `students`
- `learner_profiles`

Business service:

```text
ProfileService.create_or_update()
```

Response:

- student profile
- onboarding summary

### POST /api/chat

File:

```text
backend/app/api/routes/chat.py
```

Request schema:

```text
ChatRequest
```

Runs:

```text
AgentOrchestrator.run()
```

Response:

- tutor response
- model used
- Bloom level
- difficulty level
- misconception flag
- guiding questions

### POST /api/analyze

File:

```text
backend/app/api/routes/analyze.py
```

Request schema:

```text
AnalyzeCodeRequest
```

Runs:

```text
CodeAnalysisService.analyze()
```

Response:

- guidance
- findings
- misconception flag

The route also writes an analysis row to `chat_history`.

### GET /api/profile/{student_id}

Returns the student and learner profile.

### GET /api/dashboard/{student_id}

Returns:

- student
- Bloom progress
- weak topics
- strong topics
- recent sessions
- learning streak
- difficulty level

### GET /api/sessions/{student_id}

Returns recent learning sessions.

## 9. Learner Profiling

File:

```text
backend/app/services/profile_service.py
```

The profiler uses onboarding answers to calculate:

- `skill_score`
- `learning_level`
- `confidence_score`
- `pace_score`
- `difficulty_level`

Learning levels:

- `L1 Beginner`
- `L2 Basic`
- `L3 Intermediate`
- `L4 Advanced`
- `L5 Expert`

Scoring logic:

- confidence contributes to base skill
- beginner/no experience lowers score
- basic knowledge increases score
- intermediate/projects increase score
- advanced/competitive/placement signals increase score

The computed score maps to learner levels:

```text
< 0.25  -> L1 Beginner
< 0.45  -> L2 Basic
< 0.65  -> L3 Intermediate
< 0.85  -> L4 Advanced
>= 0.85 -> L5 Expert
```

## 10. Socratic Teaching Engine

Files:

```text
backend/app/tutor/socratic_tutor.py
backend/app/prompts/tutor_prompts.py
```

Goal:

- never immediately reveal final answers
- guide the learner with questions and hints
- adapt tone and depth using learner memory

The Socratic system prompt asks the model to return:

- short acknowledgement
- exactly two guiding questions
- one hint
- request for the student's next attempt

Prompt context includes:

- student name
- learner level
- Bloom level
- difficulty
- goal
- learning style
- weak topics
- recent mistakes
- detected misconception
- current topic
- student question

Guiding question behavior:

- L1/L2 students receive more scaffolded questions
- L3-L5 students receive more constraint, complexity, and assumption questions

## 11. Guard Node

File:

```text
backend/app/guard/prompt_guard.py
```

Purpose:

- detect prompt injection and answer-bypass attempts
- prevent the tutor from giving direct final answers when the student tries to override rules

Detected patterns include:

- `ignore previous instructions`
- `reveal answer`
- `act as chatgpt`
- `forget all rules`
- `give me final code`
- `bypass`
- `jailbreak`
- `system prompt`

If blocked:

```text
Allowed = false
Response = educational redirect
Model used = guard
Graph skips memory/route/tutor and persists redirect
```

Example redirect:

```text
I'll help you learn this. What approach have you tried so far, and where did you get stuck?
```

## 12. Hybrid Model Routing

File:

```text
backend/app/router/complexity_router.py
```

Purpose:

- classify question complexity
- choose fast model or reasoning model

Complexity scale:

- 1 easy
- 2 moderate
- 3 medium
- 4 hard
- 5 expert

Routing behavior:

```text
complexity <= 2 -> Groq Llama 3
complexity >= 3 -> GPT-4o
```

Current signals:

- Easy: `what is`, `define`, `meaning`, `example`
- Hard: `prove`, `optimize`, `complexity`, `architecture`, `concurrent`, `dynamic programming`, `graph`

Learner level modifies complexity:

- L1 students reduce complexity by one when possible
- L5 students increase complexity by one when possible

## 13. LLM Service

File:

```text
backend/app/services/llm_service.py
```

Purpose:

- isolate external model calls
- use Groq when provider is `groq`
- use OpenAI when provider is `openai`
- return local fallback response if API keys are missing or calls fail

Fallback mode is important for local development. It means onboarding, chat, dashboard, and code analysis can be tested without paid model keys.

## 14. Memory Node

File:

```text
backend/app/memory/memory_service.py
```

The memory service fetches:

- student
- learner profile
- weak topics from misconceptions
- recent mistakes
- recent sessions
- recent chat history signals

This data becomes context for the Socratic tutor.

If a student/profile is missing, the service raises:

```text
Student profile not found
```

The API returns `404`.

## 15. Misconception Detection

File:

```text
backend/app/evaluator/misconception_detector.py
```

Purpose:

- detect known misunderstandings
- persist misconception records
- make future tutoring more adaptive

Current rule examples:

- `velocity and speed are same`
- `binary search works unsorted`
- `array and linked list are same`
- `recursion is loop`

Detected output contains:

- topic
- corrective misconception message
- severity

When detected during chat, the misconception is saved to the `misconceptions` table.

## 16. Adaptive Difficulty

File:

```text
backend/app/evaluator/adaptive_evaluator.py
```

Purpose:

- increase difficulty when learner confidence is high
- reduce difficulty when a misconception is detected or confidence is low
- update Bloom level based on difficulty

Current behavior:

```text
misconception or confidence < 0.35 -> difficulty - 1
confidence > 0.75 -> difficulty + 1
otherwise -> unchanged
```

Difficulty range:

```text
1 to 5
```

Bloom mapping:

- low difficulty tends toward `Remember`
- high difficulty tends toward `Create`
- middle difficulty advances across `Understand`, `Apply`, `Analyze`, and `Evaluate`

## 17. Bloom's Taxonomy Tracking

Supported levels:

- Remember
- Understand
- Apply
- Analyze
- Evaluate
- Create

Stored on:

```text
students.current_bloom_level
```

Displayed in:

```text
ProgressPanel
```

Current MVP stores one current Bloom level per student. The dashboard maps weak topics to the student's current Bloom level.

## 18. Full Chat Workflow

This is the most important end-to-end flow.

```text
1. Student enters a question in ChatTutor.
2. ChatTutor checks that a student profile exists.
3. ChatTutor appends the student message to Zustand.
4. ChatTutor calls sendTutorMessage().
5. Axios sends POST /api/chat.
6. FastAPI validates ChatRequest with Pydantic.
7. chat.py creates AgentOrchestrator.
8. AgentOrchestrator starts LangGraph.
9. guard_node checks prompt injection.
10. If unsafe, redirect response is generated and persisted.
11. If safe, memory_node fetches student profile, weak topics, recent mistakes, and sessions.
12. route_node classifies complexity and chooses Groq or OpenAI route.
13. detect_node scans for misconceptions.
14. tutor_node builds Socratic prompt with memory and misconception context.
15. LlmService calls selected model or fallback.
16. AdaptiveEvaluator updates difficulty and Bloom level.
17. persist_node writes chat history, session, misconception if any, and updated student/profile state.
18. API returns TutorResponse.
19. ChatTutor displays response and guiding questions.
20. ChatTutor fetches dashboard.
21. ProgressPanel updates Bloom, difficulty, streak, skill score, and weak topics.
```

## 19. Full Onboarding Workflow

```text
1. Student fills onboarding form.
2. Frontend calls onboard().
3. Axios sends POST /api/onboarding.
4. FastAPI validates OnboardingRequest.
5. ProfileService computes skill score.
6. ProfileService maps skill score to L1-L5 learning level.
7. Student is created or updated by email.
8. LearnerProfile is created or updated.
9. SQLAlchemy commits the transaction.
10. API returns OnboardingResponse.
11. Frontend stores student in Zustand.
12. Chat and editor become active.
```

## 20. Full Code Analysis Workflow

```text
1. Student edits code in Monaco.
2. CodeWorkspace updates Zustand code.
3. useDebouncedEffect waits 2 seconds after changes.
4. CodeWorkspace calls analyzeCode().
5. Axios sends POST /api/analyze.
6. FastAPI validates AnalyzeCodeRequest.
7. API confirms student exists.
8. CodeAnalysisService checks language-specific issues.
9. MisconceptionDetector scans code text.
10. API writes analysis feedback to chat_history.
11. API returns CodeAnalysisResponse.
12. CodeWorkspace displays findings.
13. A workspace feedback message is also added to chat.
```

## 21. Dashboard Workflow

```text
1. Chat response completes.
2. Frontend calls fetchDashboard().
3. Axios sends GET /api/dashboard/{student_id}.
4. Backend loads student and profile.
5. Backend loads misconceptions for weak topics.
6. Backend loads recent sessions.
7. Backend returns dashboard payload.
8. Zustand dashboard state updates.
9. ProgressPanel re-renders.
```

## 22. Error Handling

Backend:

- validation errors return FastAPI/Pydantic `422`
- missing student/profile returns `404`
- profile creation failure returns `500`
- tutor engine failure returns `503`
- model call failure returns local fallback tutor response

Frontend:

- onboarding displays backend connection error
- chat displays tutor-engine offline message
- code editor displays analyzer offline message
- disabled states prevent chat before onboarding

## 23. Testing

Backend tests:

```text
backend/tests/test_api.py
backend/tests/test_guard.py
backend/tests/test_router.py
```

Coverage:

- onboarding + chat API flow
- code analysis API flow
- guard prompt injection detection
- easy question model routing
- hard question model routing

Run:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

Frontend checks:

```powershell
cd frontend
npm run typecheck
npm run lint
npm run build
```

## 24. Local Run Workflow

Start backend:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Start frontend:

```powershell
cd frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

Backend health check:

```text
http://localhost:8000/health
```

API docs:

```text
http://localhost:8000/docs
```

## 25. Current MVP Limitations

These are known MVP boundaries, not broken behavior:

- Bloom level is stored per student, not per topic in a separate table.
- Strong topics are lightly inferred and not deeply measured yet.
- Sessions are created per chat interaction and do not currently track explicit end time.
- Code analysis is static/rule-based, not a secure sandboxed code runner.
- Authentication/JWT settings exist, but auth enforcement is not implemented yet.
- LLM calls are wrapped, but advanced retry/circuit-breaker policies are minimal.
- Misconception detection is rule-based and should later be expanded with model-assisted classification.

## 26. Extension Roadmap

Recommended next engineering steps:

- add a `topic_progress` table for per-topic Bloom tracking
- add authentication and JWT-protected student routes
- add Alembic migrations instead of startup-only table creation
- add code execution sandbox for safe test-case execution
- add richer rubric-based evaluator node
- add streaming tutor responses
- add teacher/admin dashboard
- add persistent frontend session restore
- add observability logs around each LangGraph node
- add LLM retry, timeout, and fallback policies per provider

