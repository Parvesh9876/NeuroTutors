from dataclasses import dataclass


MISCONCEPTION_RULES = {
    "velocity and speed are same": ("Physics", "Velocity includes direction; speed only measures magnitude.", 3),
    "binary search works unsorted": ("Binary Search", "Binary search depends on sorted order to discard half the search space.", 3),
    "array and linked list are same": ("Data Structures", "Arrays use contiguous indexing; linked lists use nodes and references.", 2),
    "recursion is loop": ("Recursion", "Recursion calls the same function with smaller subproblems; loops repeat within one frame.", 2),
}


@dataclass(frozen=True)
class MisconceptionDetection:
    detected: bool
    topic: str | None = None
    misconception: str | None = None
    severity: int = 0


class MisconceptionDetector:
    def detect(self, text: str, topic: str) -> MisconceptionDetection:
        normalized = text.lower()
        for pattern, (rule_topic, message, severity) in MISCONCEPTION_RULES.items():
            if pattern in normalized:
                return MisconceptionDetection(True, rule_topic or topic, message, severity)
        if "same" in normalized and ("always" in normalized or "never" in normalized):
            return MisconceptionDetection(True, topic, "The answer may depend on constraints; avoid absolute rules until tested.", 1)
        return MisconceptionDetection(False)
