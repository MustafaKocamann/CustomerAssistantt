from tools.ticket_tool import TicketManagementTool
from tools.knowledge_tool import KnowledgeBaseTool
from tools.customer_tool import CustomerDatabaseTool

def test_ticket_tool():
    t = TicketManagementTool()
    created = t._run("CREATE", details={"customer_id":"CUS1"})
    status = t._run("STATUS", ticket_id=created["id"])
    assert status["status"] == "open"

def test_kb_tool():
    kb = KnowledgeBaseTool("data/knowledge_base.json")
    hits = kb._run("fatura", category="billing")
    assert len(hits) >= 1

def test_customer_db():
    db = CustomerDatabaseTool("data/customer_data.json")
    assert db._run("CUS001", "get") is not None
