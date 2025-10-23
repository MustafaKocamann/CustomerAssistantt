from .handlers import CustomerServiceStreamingHandler
from typing import Dict
import time

class InteractiveChatSystem:
    def __init__(self, handler: CustomerServiceStreamingHandler | None = None):
        self.handler = handler or CustomerServiceStreamingHandler()
        self.logs: list[Dict] = []

    def start_session(self, customer_id: str):
        self.logs.append({"event": "session_start", "customer_id": customer_id, "ts": time.time()})

    def stream_response(self, text: str):
        for tok in text.split():
            self.handler.on_llm_new_token(tok + " ")
            time.sleep(0.01)
        print()  # newline
