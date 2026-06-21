import logging
from typing import Any, Dict

_logger = logging.getLogger("crisisinfo_navigator")

if not _logger.handlers:
    _handler = logging.StreamHandler()
    _formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)


def get_logger() -> logging.Logger:
    return _logger


def log_event(event_type: str, data: Dict[str, Any]) -> None:
    """
    Log a structured event for simple observability.
    """
    _logger.info("%s | %s", event_type, data)
