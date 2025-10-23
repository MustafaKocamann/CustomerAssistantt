from main import SmartCustomerSupportSystem

def test_integration_flow():
    sys = SmartCustomerSupportSystem()
    out = sys.handle_customer_request("CUS001","Uygulamanız sürekli çöküyor, nasıl çözebilirim?")
    assert out["analysis"]["category"] == "technical"
    assert "response" in out
