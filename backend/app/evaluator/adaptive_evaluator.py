class AdaptiveEvaluator:
    def next_difficulty(self, current: int, confidence: float, misconception_detected: bool) -> int:
        if misconception_detected or confidence < 0.35:
            return max(1, current - 1)
        if confidence > 0.75:
            return min(5, current + 1)
        return current

    def next_bloom_level(self, current: str, difficulty: int) -> str:
        levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
        if difficulty <= 1:
            return "Remember"
        if difficulty >= 5:
            return "Create"
        index = levels.index(current) if current in levels else 0
        return levels[min(len(levels) - 1, max(index, difficulty))]
