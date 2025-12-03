from typing import Any, Dict
from project.core.a2a_protocol import AgentMessage, create_message
from project.core.context_engineering import build_evaluator_context
from project.memory.session_memory import SessionMemory


class Evaluator:
    """
    Evaluator agent:
    - Performs simple safety and clarity checks on the draft response.
    - Applies a light sanitization and always approves in this demo.
    """

    def __init__(self, name: str = "evaluator") -> None:
        self.name = name

    @staticmethod
    def _sanitize_text(text: str) -> str:
        """
        Very simple filter that avoids obviously medical language.
        This is a stub and not a replacement for real safety filters.
        """
        forbidden_phrases = [
            "diagnose",
            "prescription",
            "medication",
            "dose",
            "treat this condition",
        ]
        sanitized = text
        for phrase in forbidden_phrases:
            sanitized = sanitized.replace(phrase, "[redacted]")
        return sanitized

    def evaluate(
        self,
        work_message: AgentMessage,
        session_memory: SessionMemory,
    ) -> AgentMessage:
        """
        Evaluate the draft response and either approve or request changes.
        """
        context = build_evaluator_context(work_message.payload, session_memory)
        draft_payload = context["draft"]
        draft_response: str = draft_payload.get("draft_response", "")

        safe_text = self._sanitize_text(draft_response).strip()
        if not safe_text:
            safe_text = (
                "I was not able to generate guidance. "
                "Please contact your local emergency services or authorities."
            )

        eval_payload: Dict[str, Any] = {
            "status": "approved",
            "final_response": safe_text,
            "disaster_type": draft_payload.get("disaster_type"),
            "phase": draft_payload.get("phase"),
            "region": draft_payload.get("region"),
        }

        return create_message(
            sender="evaluator",
            receiver="main_agent",
            message_type="EVAL_RESPONSE",
            payload=eval_payload,
            trace_id=work_message.trace_id,
        )
