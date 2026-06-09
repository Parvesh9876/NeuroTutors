from app.router.complexity_router import ComplexityRouter


def test_easy_questions_use_fast_model():
    decision = ComplexityRouter().route("What is binary search?", "L1 Beginner", "llama", "gpt")
    assert decision.model_provider == "groq"


def test_hard_questions_use_reasoning_model():
    decision = ComplexityRouter().route("Prove graph complexity and optimize it", "L4 Advanced", "llama", "gpt")
    assert decision.model_provider == "openai"
