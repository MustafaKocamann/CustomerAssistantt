import json, os
from dotenv import load_dotenv
from chains.analysis_chain import CustomerAnalysisChain
from chains.response_chain import ResponseGenerationChain
from chains.quality_chain import QualityControlChain
from memory.hybrid_memory import HybridMemorySystem
from memory.customer_memory import CustomerProfileMemory
from tools.ticket_tool import TicketManagementTool
from tools.knowledge_tool import KnowledgeBaseTool
from tools.customer_tool import CustomerDatabaseTool
from streaming.chat_interface import InteractiveChatSystem
from streaming.handlers import CustomerServiceStreamingHandler
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


load_dotenv()

class SmartCustomerSupportSystem:
    def __init__(self):
        self.analysis = CustomerAnalysisChain()
        self.generator = ResponseGenerationChain()
        self.quality = QualityControlChain()
        self.memory = HybridMemorySystem()
        self.profile = CustomerProfileMemory()
        self.ticket = TicketManagementTool()
        self.kb = KnowledgeBaseTool()
        self.customer_db = CustomerDatabaseTool()
        self.chat = InteractiveChatSystem(CustomerServiceStreamingHandler())

        # preload customer profiles from data
        with open("data/customer_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for cid, payload in data.items():
            payload = {"customer_id": cid, **payload}
            self.profile.load(payload)

    def handle_customer_request(self, customer_id: str, message: str):
        self.chat.start_session(customer_id)
        self.memory.add_message("user", message)
        prof = self.profile.get(customer_id)

        analysis = self.analysis(message)
        articles = self.kb._run(message, category=analysis.category)
        ticket_info = None
        if analysis.urgency == "high":
            ticket_info = self.ticket._run("CREATE", details={"customer_id": customer_id, "subject": message[:60]})

        response = self.generator(analysis, message, customer_profile=prof)
        quality = self.quality(response)

        # stream the response
        self.chat.stream_response(response)

        result = {
            "analysis": analysis.model_dump(),
            "kb_hits": articles,
            "ticket": ticket_info,
            "response": response,
            "quality": quality.model_dump(),
            "memory_state": self.memory.get_state(customer_id),
        }
        return result

def demo():
    system = SmartCustomerSupportSystem()
    scenarios = [
        ("CUS001", "Uygulamanız sürekli çöküyor, nasıl çözebilirim?"),
        ("CUS002", "Bu ay faturamda garip bir ücret var, açıklayabilir misiniz?"),
        ("CUS001", "Yeni özellikler ne zaman gelecek?"),
        ("CUS002", "Bu hizmetten çok memnun değilim, iptal etmek istiyorum!"),
        ("CUS001", "Geçen hafta açtığım ticket'ın durumu nedir?"),
    ]
    for cid, msg in scenarios:
        print("\n---")
        print(f"Customer {cid}: {msg}")
        out = system.handle_customer_request(cid, msg)
        print("\n[RESULT]", json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    demo()
