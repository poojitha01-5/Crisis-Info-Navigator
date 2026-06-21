from dataclasses import dataclass, field
from typing import Any, Dict
import uuid


@dataclass
class AgentMessage:
    """
    Simple message envelope for agent-to-agent communication.
    """
    message_id: str
    trace_id: str
    sender: str
    receiver: str
    type: str
    payload: Dict[str, Any]
    meta: Dict[str, Any] = field(default_factory=dict)


def generate_trace_id() -> str:
    """
    Generate a new trace ID for a user interaction.
    """
    return str(uuid.uuid4())


def generate_message_id() -> str:
    """
    Generate a new message ID.
    """
    return str(uuid.uuid4())


def create_message(
    sender: str,
    receiver: str,
    message_type: str,
    payload: Dict[str, Any],
    trace_id: str,
    meta: Dict[str, Any] | None = None,
) -> AgentMessage:
    """
    Convenience factory for AgentMessage.
    """
    if meta is None:
        meta = {}
    return AgentMessage(
        message_id=generate_message_id(),
        trace_id=trace_id,
        sender=sender,
        receiver=receiver,
        type=message_type,
        payload=payload,
        meta=meta,
    )
