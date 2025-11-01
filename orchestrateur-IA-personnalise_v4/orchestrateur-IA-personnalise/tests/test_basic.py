from src.agents.clarifier import ClarifierAgent
from src.agents.meta_reflect import MetaReflectAgent
from src.rag.retriever import TFIDFRetriever
import os

def test_clarifier():
    c = ClarifierAgent()
    qs = c.ask("Plan marketing")
    assert isinstance(qs, list)

def test_meta_reflect():
    m = MetaReflectAgent()
    r = m.score({"answer": "Réponse courte.\n\n- point", "evidence": [{"text":"x","source":"y"}]})
    assert r["score"] >= 0.5

def test_retriever_build(tmp_path):
    # Build a tiny index
    d = tmp_path / "docs"
    d.mkdir()
    (d / "a.md").write_text("# Titre\nL'orchestrateur coordonne des agents.", encoding="utf-8")
    from scripts.build_index import main as build_main  # type: ignore
    import sys
    sys.argv = ["", "--input", str(d), "--index", str(tmp_path / "index.pkl")]
    build_main()
    r = TFIDFRetriever(index_path=str(tmp_path / "index.pkl"))
    results = r.search("orchestrateur agents", k=2)
    assert isinstance(results, list)
