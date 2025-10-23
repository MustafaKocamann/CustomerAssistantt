from pydantic import BaseModel
import re

class QualityReport(BaseModel):
    score: float
    suggestions: list[str]

class QualityControlChain:
    """
    Lightweight quality scorer based on heuristics.
    """
    def __call__(self, response: str) -> QualityReport:
        score = 8.0
        suggestions = []
        if len(response) < 60:
            score -= 1.0
            suggestions.append("Yanıt çok kısa; adımları detaylandırın.")
        if not response.strip().endswith(("?", ".", "!")):
            score -= 0.5
            suggestions.append("Noktalama ile sonlandırın.")
        if not re.search(r"(üzgün|sorry|özür)", response, flags=re.I):
            suggestions.append("Empati cümlesi eklemeyi düşünün.")
            score -= 0.3
        score = max(0.0, min(10.0, score))
        return QualityReport(score=score, suggestions=suggestions)
