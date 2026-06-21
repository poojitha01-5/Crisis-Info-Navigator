from typing import Any, Dict
from project.core.a2a_protocol import AgentMessage, create_message
from project.core.context_engineering import build_planner_context
from project.memory.session_memory import SessionMemory


class Planner:
    """
    Planner agent:
    - Classifies disaster type using simple keyword heuristics.
    - Classifies phase (preparedness / during / recovery).
    - Creates a simple plan for downstream agents.
    """

    def __init__(self, name: str = "planner") -> None:
        self.name = name

    @staticmethod
    def _detect_disaster_type(text: str) -> str:
        text_lower = text.lower()
        if "earthquake" in text_lower:
            return "earthquake"
        if "flood" in text_lower or "flooding" in text_lower:
            return "flood"
        if "cyclone" in text_lower or "hurricane" in text_lower or "typhoon" in text_lower:
            return "cyclone"
        if "fire" in text_lower or "wildfire" in text_lower:
            return "fire"
        if "heatwave" in text_lower or "heat wave" in text_lower or "extreme heat" in text_lower:
            return "heatwave"
        if "landslide" in text_lower or "mudslide" in text_lower:
            return "landslide"
        # Fallback for any other or unknown hazard
        return "generic"

    @staticmethod
    def _detect_phase(text: str) -> str:
        text_lower = text.lower()
        if any(word in text_lower for word in ["now", "right now", "happening", "currently", "during"]):
            return "during"
        if any(word in text_lower for word in ["after", "aftermath", "recovery", "post"]):
            return "recovery"
        if any(word in text_lower for word in ["prepare", "before", "ready", "readiness", "might happen"]):
            return "preparedness"
        # Default to preparedness if not clear
        return "preparedness"

    def plan(
        self,
        user_input: str,
        session_memory: SessionMemory,
        trace_id: str,
    ) -> AgentMessage:
        """
        Create a high-level plan for the Worker.
        """
        context = build_planner_context(user_input, session_memory)
        disaster_type = self._detect_disaster_type(user_input)
        phase = self._detect_phase(user_input)

        user_profile = context.get("user_profile", {})
        region = user_profile.get("region", "generic")

        plan_payload: Dict[str, Any] = {
            "disaster_type": disaster_type,
            "phase": phase,
            "region": region,
            "objectives": [
                "Provide concise, step-by-step non-medical safety guidance.",
                "Mention emergency hotlines if available.",
            ],
            "tool_calls": [
                "generate_disaster_guidance_llm",
                "hotline_lookup",
            ],
            "raw_user_input": user_input,
        }

        state = session_memory.get_state()
        state["last_disaster_type"] = disaster_type
        state["last_phase"] = phase
        session_memory.update_state(**state)

        return create_message(
            sender="planner",
            receiver="worker",
            message_type="PLAN_RESPONSE",
            payload=plan_payload,
            trace_id=trace_id,
        )
