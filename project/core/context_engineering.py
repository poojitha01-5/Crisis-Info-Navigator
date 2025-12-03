from typing import Any, Dict
from project.memory.session_memory import SessionMemory


def build_planner_context(user_input: str, memory: SessionMemory) -> Dict[str, Any]:
    """
    Build a context structure for the Planner agent.
    """
    user_profile = memory.get_user_profile()
    state = memory.get_state()

    return {
        "user_input": user_input,
        "user_profile": user_profile,
        "state": state,
        "system_policy": {
            "non_medical": True,
            "safety_first": True,
            "disaster_phases": ["preparedness", "during", "recovery"],
        },
    }


def build_worker_context(plan_payload: Dict[str, Any], memory: SessionMemory) -> Dict[str, Any]:
    """
    Build a context structure for the Worker agent.
    """
    user_profile = memory.get_user_profile()
    state = memory.get_state()
    return {
        "plan": plan_payload,
        "user_profile": user_profile,
        "state": state,
    }


def build_evaluator_context(
    work_payload: Dict[str, Any], memory: SessionMemory
) -> Dict[str, Any]:
    """
    Build a context structure for the Evaluator agent.
    """
    user_profile = memory.get_user_profile()
    state = memory.get_state()
    return {
        "draft": work_payload,
        "user_profile": user_profile,
        "state": state,
        "checks": {
            "non_medical": True,
            "clarity": True,
            "source_alignment": True,
        },
    }
