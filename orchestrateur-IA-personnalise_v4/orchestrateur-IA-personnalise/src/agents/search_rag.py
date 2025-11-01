from ..schemas.models import Brief, Evidence
from ..rag.hybrid import HybridRetriever

class RAGAgent:
    def __init__(self, index_path: str = "data/index.pkl", alpha: float = 0.5):
        self.retriever = HybridRetriever(index_path=index_path, alpha=alpha)

    def retrieve(self, brief: Brief):
        q = ((brief.objectif or "") + " " + (brief.contexte or "")).strip() or "orchestrateur agents citations"
        hits = self.retriever.search(q, k=6)
        return [Evidence(text=h["text"], source=h["source"]) for h in hits]
