from typing import Any, Dict
from project.core.a2a_protocol import AgentMessage, create_message
from project.core.context_engineering import build_worker_context
from project.memory.session_memory import SessionMemory
from project.tools import tools as tool_module


class Worker:
    """
    Worker agent:
    - Executes the plan produced by the Planner.
    - Calls Google Gemini via tools.generate_disaster_guidance_llm
      to get dynamic, non-hardcoded safety guidance.
    - Also adds hotline information where possible.
    """

    def __init__(self, name: str = "worker") -> None:
        self.name = name

    @staticmethod
    def _format_hotlines(hotlines: Dict[str, str]) -> str:
        if not hotlines:
            return ""
        lines = ["", "Emergency contacts (verify for your exact location):"]
        for key, value in hotlines.items():
            label = key.replace("_", " ").title()
            lines.append(f"- {label}: {value}")
        return "\n".join(lines)

    def execute(
        self,
        plan_message: AgentMessage,
        session_memory: SessionMemory,
    ) -> AgentMessage:
        """
        Execute the Planner's plan and generate a draft response.
        """
        context = build_worker_context(plan_message.payload, session_memory)
        plan = context["plan"]

        disaster_type = plan.get("disaster_type", "generic")
        phase = plan.get("phase", "preparedness")
        region = plan.get("region", "generic")
        raw_user_input = plan.get("raw_user_input", "")

        # Call Gemini to dynamically generate guidance text
        guidance_text = tool_module.generate_disaster_guidance_llm(
            disaster_type=disaster_type,
            phase=phase,
            region=region,
            raw_input=raw_user_input,
        )

        hotlines = tool_module.hotline_lookup(region)
        hotline_text = self._format_hotlines(hotlines)

        header = f"Here is some basic non-medical guidance for a {disaster_type} ({phase} phase):"
        draft_response = f"{header}\n\n{guidance_text}{hotline_text}"

        draft_payload: Dict[str, Any] = {
            "draft_response": draft_response,
            "disaster_type": disaster_type,
            "phase": phase,
            "region": region,
            "raw_user_input": raw_user_input,
        }

        return create_message(
            sender="worker",
            receiver="evaluator",
            message_type="WORK_RESPONSE",
            payload=draft_payload,
            trace_id=plan_message.trace_id,
        )
