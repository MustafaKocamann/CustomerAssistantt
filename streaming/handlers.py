from typing import Callable

class CustomerServiceStreamingHandler:
    """
    Simple streaming printer; wire this into your LLM callbacks if desired.
    """
    def __init__(self, on_token: Callable[[str], None] | None = None):
        self.on_token = on_token or (lambda t: print(t, end="", flush=True))

    def on_llm_new_token(self, token: str, **kwargs):
        # Progressive response + simple typing indicator
        self.on_token(token)
