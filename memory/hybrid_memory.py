from __future__ import annotations
from collections import deque
from typing import Dict, Any

class HybridMemorySystem:
    """
    - summary: rolling summary (string)
    - window: last 5 messages
    - metadata: arbitrary customer metadata
    """
    def __init__(self):
        self.summary: str = ""
        self.window: deque[dict] = deque(maxlen=5)
        self.metadata: Dict[str, Any] = {}

    def add_message(self, role: str, content: str):
        self.window.append({"role": role, "content": content})
        # naive summarization
        self.summary = (self.summary + " " + content).strip()[-1000:]

    def set_customer_meta(self, customer_id: str, **kwargs):
        self.metadata.setdefault(customer_id, {}).update(kwargs)

    def get_state(self, customer_id: str) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "recent_window": list(self.window),
            "metadata": self.metadata.get(customer_id, {}),
        }

    def optimize(self):
        # naive compaction
        if len(self.summary) > 800:
            self.summary = self.summary[-800:]
