from dataclasses import dataclass


HARD_SIGNALS = ("prove", "optimize", "complexity", "architecture", "concurrent", "dynamic programming", "graph")
EASY_SIGNALS = ("what is", "define", "meaning", "example")


@dataclass(frozen=True)
class RouteDecision:
    complexity: int
    model_provider: str
    model_name: str


class ComplexityRouter:
    def route(self, question: str, student_level: str, configured_fast: str, configured_reasoning: str) -> RouteDecision:
        text = question.lower()
        complexity = 3
        if any(signal in text for signal in EASY_SIGNALS):
            complexity = 1
        if any(signal in text for signal in HARD_SIGNALS):
            complexity = 4
        if "L1" in student_level and complexity > 1:
            complexity -= 1
        if "L5" in student_level and complexity < 5:
            complexity += 1
        if complexity <= 2:
            return RouteDecision(complexity=complexity, model_provider="groq", model_name=configured_fast)
        return RouteDecision(complexity=complexity, model_provider="openai", model_name=configured_reasoning)
