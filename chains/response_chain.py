from typing import Dict
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os, traceback

from .analysis_chain import AnalysisResult

class ResponseGenerationChain:
    """
    Generates an intelligent customer response using OpenAI's GPT model.
    Falls back to templates if API fails.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            api_key=api_key,
        )
        self.prompt = ChatPromptTemplate.from_template("""
        Sen bir müşteri destek temsilcisisin.
        Aşağıdaki analiz sonuçlarına ve müşteri profiline göre profesyonel, empatik ve açıklayıcı bir yanıt oluştur.

        🧾 Müşteri Mesajı:
        {message}

        🧩 Analiz Özeti:
        {analysis}

        👤 Müşteri Profili:
        {customer_profile}

        Kurallar:
        - Türkçe yanıt ver.
        - Kibar, doğal ve güven veren bir ton kullan.
        - Gereksiz uzunlukta olmasın ama eksik bilgi bırakma.
        - Teknik sorularda adım adım öneri sun.
        - Faturalama veya üyelik konularında çözüm sürecini belirt.
        - Genel sorularda bilgi verici bir ton kullan.
        """)

    def __call__(self, analysis: AnalysisResult, message: str, customer_profile: Dict | None = None) -> str:
        try:
            messages = self.prompt.format_messages(
                message=message,
                analysis=analysis.model_dump(),
                customer_profile=customer_profile or {}
            )
            response = self.llm.invoke(messages)
            return response.content.strip()

        except Exception as e:
            # 🔴 DEBUG BLOĞU
            print("\n❌ GPT çağrısı başarısız oldu!")
            print("Hata türü:", type(e).__name__)
            print("Detay:", e)
            print("Traceback:")
            traceback.print_exc()
            print("⚠️ Fallback yanıt devreye alındı.\n")

            # Fallback: eski sistem
            style = (customer_profile or {}).get("preferred_style", "neutral")
            prefix = {
                "empathetic": "Üzgünüz, yaşadığınız sorun için üzgünüz. ",
                "concise": "",
                "neutral": ""
            }.get(style, "")
            if analysis.category == "technical":
                body = "Aşağıdaki adımları deneyebilir misiniz: önbelleği temizleyin, uygulamayı güncelleyin, fotoğraf boyutu 10MB altında olsun, güvenli modda deneyin."
            elif analysis.category == "billing":
                body = "Faturanızı ve eklentilerinizi kontrol edelim. Hesap e-postanızı ve ilgili işlem tarihini paylaşır mısınız? Gerekirse iade politikamızı uygulayabiliriz."
            else:
                body = "Yeni özellikler için yol haritamız iki haftada bir küçük, üç ayda bir büyük yayınlar içerir. İlginizi çeken özellik varsa not edelim."
            closing = " Başka yardımcı olabileceğimiz bir konu var mı?"
            return f"{prefix}{body}{closing}"
