from typing import Any, Dict
from project.agents.planner import Planner
from project.agents.worker import Worker
from project.agents.evaluator import Evaluator
from project.core.a2a_protocol import generate_trace_id
from project.core.observability import log_event
from project.memory.session_memory import SessionMemory


class MainAgent:
    """
    Orchestrates the Planner -> Worker -> Evaluator multi-agent flow.
    """

    def __init__(self, session_id: str = "default") -> None:
        self.session_memory = SessionMemory(session_id=session_id)
        self.planner = Planner()
        self.worker = Worker()
        self.evaluator = Evaluator()

    def handle_message(self, user_input: str) -> Dict[str, Any]:
        """
        Handle a single user message through the multi-agent pipeline.
        """
        trace_id = generate_trace_id()
        log_event("user_message", {"trace_id": trace_id, "user_input": user_input})

        plan_msg = self.planner.plan(user_input, self.session_memory, trace_id)
        log_event("plan_created", {"trace_id": trace_id, "plan": plan_msg.payload})

        work_msg = self.worker.execute(plan_msg, self.session_memory)
        log_event("work_completed", {"trace_id": trace_id, "work": work_msg.payload})

        eval_msg = self.evaluator.evaluate(work_msg, self.session_memory)
        log_event("evaluation_completed", {"trace_id": trace_id, "evaluation": eval_msg.payload})

        final_text = eval_msg.payload.get("final_response", "No response generated.")

        return {
            "response": final_text,
            "trace_id": trace_id,
            "disaster_type": eval_msg.payload.get("disaster_type"),
            "phase": eval_msg.payload.get("phase"),
            "region": eval_msg.payload.get("region"),
        }


def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]
