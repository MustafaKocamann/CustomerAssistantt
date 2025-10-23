from memory.hybrid_memory import HybridMemorySystem
from memory.customer_memory import CustomerProfileMemory

def test_hybrid_memory():
    m = HybridMemorySystem()
    for i in range(6):
        m.add_message("user", f"msg {i}")
    st = m.get_state("CUS001")
    assert len(st["recent_window"]) == 5

def test_customer_profile():
    c = CustomerProfileMemory()
    c.load({"customer_id":"CUSX","preferred_style":"empathetic"})
    assert c.get("CUSX")["preferred_style"] == "empathetic"
