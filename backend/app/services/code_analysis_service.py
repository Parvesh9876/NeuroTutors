import ast

from app.evaluator.misconception_detector import MisconceptionDetector


class CodeAnalysisService:
    def __init__(self):
        self.detector = MisconceptionDetector()

    def analyze(self, code: str, language: str, topic: str) -> tuple[str, list[str], bool]:
        findings: list[str] = []
        if language == "python":
            try:
                ast.parse(code)
            except SyntaxError as exc:
                findings.append(f"Python syntax issue near line {exc.lineno}: {exc.msg}")
        if language == "java":
            if "class " not in code:
                findings.append("Java programs usually need a class wrapper for executable code.")
            if code.count("{") != code.count("}"):
                findings.append("Brace counts do not match; check block boundaries.")
        if "while true" in code.lower() or "while(True)" in code:
            findings.append("Possible infinite loop. What condition should eventually stop the loop?")
        if not findings:
            findings.append("No obvious syntax issue found. Now test the logic with a small input.")
        detection = self.detector.detect(code, topic)
        guidance = (
            "Good, let's inspect the code like a teacher would. "
            f"{findings[0]} "
            "What value changes at each step, and what invariant should remain true?"
        )
        return guidance, findings, detection.detected
