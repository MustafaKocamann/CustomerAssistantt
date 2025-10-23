import json
from typing import Dict, Any, Literal

class CustomerDatabaseTool:
    name = "customer_db"
    description = "Müşteri bilgilerini sorgular ve günceller"

    def __init__(self, path: str = "data/customer_data.json"):
        self.path = path
        with open(path, "r", encoding="utf-8") as f:
            self.db: Dict[str, Dict[str, Any]] = json.load(f)

    def _persist(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)

    def _run(self, customer_id: str, action: Literal["get","update","history"]="get", payload: Dict[str, Any] | None = None):
        if action == "get":
            return self.db.get(customer_id)
        if action == "history":
            return self.db.get(customer_id, {}).get("history", [])
        if action == "update":
            self.db.setdefault(customer_id, {}).update(payload or {})
            self._persist()
            return self.db[customer_id]
        raise ValueError("Unknown action")
