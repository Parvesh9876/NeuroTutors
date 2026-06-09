from app.memory.memory_service import LearningMemory


class SocraticTutor:
    def build_prompt(self, question: str, topic: str, memory: LearningMemory, misconception: str | None) -> str:
        return f"""
Student: {memory.student.name}
Level: {memory.student.learning_level}
Bloom Level: {memory.student.current_bloom_level}
Difficulty: {memory.profile.difficulty_level}
Goal: {memory.profile.goal}
Learning Style: {memory.profile.preferred_learning_style}
Weak Topics: {", ".join(memory.weak_topics) or "None yet"}
Recent Mistakes: {"; ".join(memory.recent_mistakes) or "None yet"}
Detected Misconception: {misconception or "None"}
Topic: {topic}
Student Question: {question}

Generate adaptive Socratic tutoring. Never reveal the final answer.
"""

    def guiding_questions(self, student_level: str, topic: str) -> list[str]:
        if "L1" in student_level or "L2" in student_level:
            return [
                f"What condition or definition do we need before using {topic}?",
                "Can you try a tiny example and describe what happens step by step?",
            ]
        return [
            f"Why do the constraints of {topic} make this approach valid?",
            "What changes in time or space complexity if one key assumption is removed?",
        ]
