from typing import Optional, Dict, List
from uuid import uuid4

class TicketManagementTool:
    name = "ticket_manager"
    description = "Destek bileti oluşturur, günceller ve takip eder"

    def __init__(self):
        self._tickets: Dict[str, Dict] = {}

    def _run(self, action: str, ticket_id: Optional[str] = None, details: Optional[Dict] = None):
        action = action.upper()
        if action == "CREATE":
            tid = f"TKT{uuid4().hex[:10].upper()}"
            self._tickets[tid] = {"id": tid, "status": "open", "details": details or {}}
            return self._tickets[tid]
        if action == "UPDATE":
            if not ticket_id or ticket_id not in self._tickets:
                raise ValueError("Ticket not found")
            self._tickets[ticket_id].update(details or {})
            return self._tickets[ticket_id]
        if action == "STATUS":
            if not ticket_id or ticket_id not in self._tickets:
                raise ValueError("Ticket not found")
            return {"id": ticket_id, "status": self._tickets[ticket_id]["status"]}
        if action == "LIST":
            cust = (details or {}).get("customer_id")
            items = list(self._tickets.values())
            if cust:
                items = [t for t in items if t.get("details", {}).get("customer_id") == cust]
            return items
        raise ValueError("Unknown action")
