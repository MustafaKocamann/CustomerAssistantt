from typing import Dict, Any

class CustomerProfileMemory:
    def __init__(self):
        self._profiles: Dict[str, Dict[str, Any]] = {}

    def load(self, profile: Dict[str, Any]):
        cid = profile.get("id") or profile.get("customer_id")
        if not cid:
            raise ValueError("profile must include id or customer_id")
        self._profiles[cid] = profile

    def get(self, customer_id: str) -> Dict[str, Any]:
        return self._profiles.get(customer_id, {"preferred_style": "neutral", "history": []})

    def update(self, customer_id: str, **updates):
        prof = self._profiles.setdefault(customer_id, {})
        prof.update(updates)
        return prof

    def report(self) -> Dict[str, Any]:
        return {"count": len(self._profiles), "keys": list(self._profiles.keys())}
