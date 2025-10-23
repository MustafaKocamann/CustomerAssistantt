from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os
import json

Category = Literal["technical", "billing", "general"]

class AnalysisResult(BaseModel):
    category: Category
    urgency: Literal["low", "medium", "high"]
    tone: Literal["neutral", "frustrated", "angry", "curious"]
    language: str = Field(default="tr")

class CustomerAnalysisChain:
    """
    LLM destekli müşteri mesajı analiz zinciri.
    GPT modeliyle mesajın kategori, aciliyet, ton ve dilini belirler.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=api_key
        )

    def __call__(self, message: str) -> AnalysisResult:
        prompt = f"""
        Aşağıdaki müşteri mesajını analiz et ve sadece JSON formatında cevap ver.
        Alanlar: category (technical/billing/general), urgency (low/medium/high), tone (neutral/frustrated/angry/curious), language (tr/en/other).

        Mesaj: "{message}"

        Örnek çıktı formatı:
        {{
          "category": "technical",
          "urgency": "high",
          "tone": "frustrated",
          "language": "tr"
        }}
        """

        try:
            res = self.llm.invoke(prompt)
            content = res.content.strip()
            data = json.loads(content)
        except Exception as e:
            print("⚠️ LLM analiz hatası:", e)
            # fallback – eski heuristic yapı
            data = {"category": "general", "urgency": "medium", "tone": "neutral", "language": "tr"}

        return AnalysisResult(**data)
