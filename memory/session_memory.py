from typing import Any, Dict


class SessionMemory:
    """
    Extremely simple in-memory session + user-profile storage.

    In a real deployment this would be backed by Redis, a database, or another
    external store. For the demo, it is process-local.
    """

    _sessions: Dict[str, Dict[str, Any]] = {}

    def __init__(self, session_id: str = "default") -> None:
        self.session_id = session_id
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "user_profile": {},
                "state": {},
            }

    # ---- User profile -----------------------------------------------------
    def get_user_profile(self) -> Dict[str, Any]:
        return self._sessions[self.session_id]["user_profile"]

    def update_user_profile(self, **kwargs: Any) -> None:
        self._sessions[self.session_id]["user_profile"].update(kwargs)

    # ---- Session state -----------------------------------------------------
    def get_state(self) -> Dict[str, Any]:
        return self._sessions[self.session_id]["state"]

    def update_state(self, **kwargs: Any) -> None:
        self._sessions[self.session_id]["state"].update(kwargs)
