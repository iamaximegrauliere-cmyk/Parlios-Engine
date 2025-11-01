from ..schemas.models import Brief, OrchestratorResponse
from ..agents.briefing import BriefingAgent
from ..agents.clarifier import ClarifierAgent
from ..agents.meta_reflect import MetaReflectAgent
from ..agents.search_rag import RAGAgent
from ..agents.producer import ProducerAgent
from ..agents.verifier import VerifierAgent
from ..memory.profile_store import ProfileStore

class Orchestrator:
    def __init__(self):
        self.profile = ProfileStore()
        self.briefing = BriefingAgent(self.profile)
        self.clarifier = ClarifierAgent()
        self.meta = MetaReflectAgent()
        self.rag = RAGAgent()
        self.producer = ProducerAgent(self.profile)
        self.verifier = VerifierAgent()

    def make_brief(self, prompt_fluide: str) -> dict:
        # 0) clarification
        qs = self.clarifier.ask(prompt_fluide)
        if qs:
            return {"needs_clarification": True, "questions": qs, "original": prompt_fluide}
        brief = self.briefing.from_fuzzy(prompt_fluide)
        return brief.model_dump()

    def run_brief(self, brief_dict: dict) -> dict:
        # Handle case when clarification is required
        if brief_dict.get("needs_clarification"):
            return {"status": "clarification_required", **brief_dict}
        brief = Brief(**brief_dict)
        # 1) Retrieve evidence
        evidence = self.rag.retrieve(brief)
        # 2) Produce with style alignment
        draft = self.producer.produce(brief, evidence)
        # 3) Verify against criteria
        verdict = self.verifier.check(brief, draft, evidence)
        # 4) Meta-reflection score
        meta = self.meta.score(draft)
        # 5) Store simple metrics in profile
        self.profile.record_metrics({"last_meta_score": meta.get("score", 0), "citations": bool(evidence)})
        return OrchestratorResponse(brief=brief, evidence=evidence, draft=draft, verdict=verdict).model_dump() | {"meta": meta}

    def ask(self, question: str, profile_overrides: dict | None = None) -> dict:
        if profile_overrides:
            self.profile.update_overrides(profile_overrides)
        brief = self.briefing.from_fuzzy(question)
        return self.run_brief(brief.model_dump())

    def verify(self, brief: dict, response: dict) -> dict:
        b = Brief(**brief)
        v = self.verifier.check(b, response, response.get("evidence", []))
        return v

    def profile_event(self, event: str, payload: dict) -> dict:
        return self.profile.ingest_event(event, payload)
