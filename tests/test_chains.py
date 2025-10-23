from chains.analysis_chain import CustomerAnalysisChain
from chains.response_chain import ResponseGenerationChain
from chains.quality_chain import QualityControlChain

def test_analysis():
    ac = CustomerAnalysisChain()
    r1 = ac("Uygulama çöküyor")
    assert r1.category == "technical"
    r2 = ac("Faturamda garip ücret")
    assert r2.category == "billing"

def test_response_quality():
    gen = ResponseGenerationChain()
    qc = QualityControlChain()
    text = gen(ac := type("A", (), {"category":"technical","urgency":"high","tone":"frustrated","language":"tr"})(), "msg")
    rep = qc(text)
    assert rep.score <= 10.0
