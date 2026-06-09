from dataclasses import dataclass

from langchain_core.messages import HumanMessage, SystemMessage

from app.config.settings import Settings


@dataclass(frozen=True)
class LlmResult:
    text: str
    model_used: str


class LlmService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def generate(self, system_prompt: str, user_prompt: str, provider: str, model: str) -> LlmResult:
        try:
            if provider == "groq" and self.settings.groq_api_key:
                from langchain_groq import ChatGroq

                llm = ChatGroq(model=model, api_key=self.settings.groq_api_key, timeout=self.settings.request_timeout_seconds)
                response = await llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
                return LlmResult(text=str(response.content), model_used=model)
            if provider == "openai" and self.settings.openai_api_key:
                from langchain_openai import ChatOpenAI

                llm = ChatOpenAI(model=model, api_key=self.settings.openai_api_key, timeout=self.settings.request_timeout_seconds)
                response = await llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
                return LlmResult(text=str(response.content), model_used=model)
        except Exception:
            return LlmResult(text=self._fallback_response(user_prompt), model_used=f"{model}-fallback")
        return LlmResult(text=self._fallback_response(user_prompt), model_used=f"{model}-local")

    def _fallback_response(self, user_prompt: str) -> str:
        return (
            "Let's reason through it together.\n\n"
            "1. What facts or constraints do you already know from the problem?\n"
            "2. Which part feels uncertain: the concept, the steps, or the implementation?\n\n"
            "Hint: try a tiny example first and describe what changes after each step.\n\n"
            "Send your next attempt, and I will help you refine it."
        )
