from dataclasses import dataclass


INJECTION_PATTERNS = (
    "ignore previous instructions",
    "reveal answer",
    "act as chatgpt",
    "forget all rules",
    "give me final code",
    "bypass",
    "jailbreak",
    "system prompt",
)


@dataclass(frozen=True)
class GuardResult:
    allowed: bool
    reason: str | None = None
    redirect: str | None = None


class PromptGuard:
    def inspect(self, text: str) -> GuardResult:
        normalized = text.lower()
        matched = next((pattern for pattern in INJECTION_PATTERNS if pattern in normalized), None)
        if matched:
            return GuardResult(
                allowed=False,
                reason=f"Detected unsafe tutoring bypass: {matched}",
                redirect="I'll help you learn this. What approach have you tried so far, and where did you get stuck?",
            )
        return GuardResult(allowed=True)
