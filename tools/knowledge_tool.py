import json, os
from typing import Optional, List, Dict

class KnowledgeBaseTool:
    name = "knowledge_base"
    description = "Şirket bilgi tabanından ilgili makaleleri bulur"

    def __init__(self, kb_path: str = "data/knowledge_base.json"):
        self.kb_path = kb_path
        with open(kb_path, "r", encoding="utf-8") as f:
            self.kb: List[Dict] = json.load(f)

    def _run(self, query: str, category: Optional[str] = None) -> List[Dict]:
        q = query.lower()
        def score(item: Dict) -> int:
            title = item["title"].lower()
            tags = " ".join(item.get("tags", [])).lower()
            base = 0
            if q in title: base += 3
            if q in item["content"].lower(): base += 2
            if any(q in t for t in tags.split()): base += 1
            if category and item.get("category") == category:
                base += 2
            return base
        ranked = sorted(self.kb, key=score, reverse=True)
        return [r for r in ranked if score(r) > 0][:5]
