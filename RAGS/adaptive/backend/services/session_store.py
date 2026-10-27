"""Bounded, in-memory conversation history per frontend session.

Each session keeps at most ``max_turns`` question/answer pairs; idle sessions
expire after ``ttl_minutes`` and the least recently used are evicted beyond
``max_sessions``. Sessions are isolated by id and nothing is persisted.
"""

import threading
import time
from collections import OrderedDict, deque

_MAX_STORED_ANSWER_CHARS = 1500


class SessionStore:
    def __init__(self, max_turns: int, max_sessions: int, ttl_minutes: int) -> None:
        self._max_messages = max_turns * 2
        self._max_sessions = max_sessions
        self._ttl_seconds = ttl_minutes * 60
        self._sessions: OrderedDict[str, tuple[float, deque[dict[str, str]]]] = OrderedDict()
        self._lock = threading.Lock()

    def _evict_expired(self, now: float) -> None:
        expired = [key for key, (seen, _) in self._sessions.items() if now - seen > self._ttl_seconds]
        for key in expired:
            del self._sessions[key]

    def get_history(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            self._evict_expired(time.monotonic())
            entry = self._sessions.get(session_id)
            return [dict(message) for message in entry[1]] if entry else []

    def append_turn(self, session_id: str, question: str, answer: str) -> None:
        if self._max_messages == 0:
            return
        with self._lock:
            now = time.monotonic()
            _, messages = self._sessions.pop(session_id, (now, deque(maxlen=self._max_messages)))
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": answer[:_MAX_STORED_ANSWER_CHARS]})
            self._sessions[session_id] = (now, messages)
            while len(self._sessions) > self._max_sessions:
                self._sessions.popitem(last=False)

    def clear(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None
