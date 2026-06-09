from sqlalchemy.orm import Session

from langgraph.graph import END, StateGraph

from app.agents.state import TutorState
from app.config.settings import Settings
from app.evaluator.adaptive_evaluator import AdaptiveEvaluator
from app.evaluator.misconception_detector import MisconceptionDetector
from app.guard.prompt_guard import PromptGuard
from app.memory.memory_service import MemoryService
from app.models import ChatHistory, Misconception, SessionRecord
from app.prompts.tutor_prompts import SOCRATIC_SYSTEM_PROMPT
from app.router.complexity_router import ComplexityRouter
from app.services.llm_service import LlmService
from app.tutor.socratic_tutor import SocraticTutor


class AgentOrchestrator:
    def __init__(self, db: Session, settings: Settings):
        self.db = db
        self.settings = settings
        self.guard = PromptGuard()
        self.router = ComplexityRouter()
        self.memory = MemoryService()
        self.detector = MisconceptionDetector()
        self.evaluator = AdaptiveEvaluator()
        self.tutor = SocraticTutor()
        self.llm = LlmService(settings)
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(TutorState)
        graph.add_node("guard_node", self._guard_node)
        graph.add_node("memory_node", self._memory_node)
        graph.add_node("route_node", self._route_node)
        graph.add_node("detect_node", self._detect_node)
        graph.add_node("tutor_node", self._tutor_node)
        graph.add_node("persist_node", self._persist_node)
        graph.set_entry_point("guard_node")
        graph.add_conditional_edges("guard_node", lambda state: "persist_node" if not state["guarded"] else "memory_node")
        graph.add_edge("memory_node", "route_node")
        graph.add_edge("route_node", "detect_node")
        graph.add_edge("detect_node", "tutor_node")
        graph.add_edge("tutor_node", "persist_node")
        graph.add_edge("persist_node", END)
        return graph.compile()

    async def run(self, student_id: int, question: str, topic: str) -> TutorState:
        return await self.graph.ainvoke({"student_id": student_id, "question": question, "topic": topic})

    def _guard_node(self, state: TutorState) -> TutorState:
        result = self.guard.inspect(state["question"])
        state["guarded"] = result.allowed
        if not result.allowed:
            state["redirect"] = result.redirect or "Let's keep this focused on learning. What have you tried?"
            state["response"] = state["redirect"]
            state["model_used"] = "guard"
            state["misconception_detected"] = False
            state["guiding_questions"] = ["What approach have you tried?", "Where did your reasoning get stuck?"]
        return state

    def _memory_node(self, state: TutorState) -> TutorState:
        state["memory"] = self.memory.fetch(self.db, state["student_id"])
        return state

    def _route_node(self, state: TutorState) -> TutorState:
        memory = state["memory"]
        decision = self.router.route(state["question"], memory.student.learning_level, self.settings.fast_model, self.settings.reasoning_model)
        state["complexity"] = decision.complexity
        state["provider"] = decision.model_provider
        state["model"] = decision.model_name
        return state

    def _detect_node(self, state: TutorState) -> TutorState:
        detection = self.detector.detect(state["question"], state["topic"])
        state["misconception_detected"] = detection.detected
        if detection.detected:
            state["misconception"] = detection.misconception or ""
            state["severity"] = detection.severity
        return state

    async def _tutor_node(self, state: TutorState) -> TutorState:
        memory = state["memory"]
        prompt = self.tutor.build_prompt(state["question"], state["topic"], memory, state.get("misconception"))
        result = await self.llm.generate(SOCRATIC_SYSTEM_PROMPT, prompt, state["provider"], state["model"])
        next_difficulty = self.evaluator.next_difficulty(
            memory.profile.difficulty_level,
            memory.student.confidence_score,
            state["misconception_detected"],
        )
        state["response"] = result.text
        state["model_used"] = result.model_used
        state["guiding_questions"] = self.tutor.guiding_questions(memory.student.learning_level, state["topic"])
        state["difficulty_level"] = next_difficulty
        state["bloom_level"] = self.evaluator.next_bloom_level(memory.student.current_bloom_level, next_difficulty)
        return state

    def _persist_node(self, state: TutorState) -> TutorState:
        student = self.memory.fetch(self.db, state["student_id"]).student
        student.current_bloom_level = state.get("bloom_level", student.current_bloom_level)
        if student.profile:
            student.profile.difficulty_level = state.get("difficulty_level", student.profile.difficulty_level)
        if state.get("misconception_detected"):
            self.db.add(
                Misconception(
                    student_id=state["student_id"],
                    topic=state["topic"],
                    misconception=state.get("misconception", "Possible conceptual misunderstanding"),
                    severity=state.get("severity", 1),
                )
            )
        self.db.add(SessionRecord(student_id=state["student_id"], topic=state["topic"]))
        self.db.add(
            ChatHistory(
                student_id=state["student_id"],
                question=state["question"],
                response=state["response"],
                model_used=state["model_used"],
            )
        )
        self.db.commit()
        return state
