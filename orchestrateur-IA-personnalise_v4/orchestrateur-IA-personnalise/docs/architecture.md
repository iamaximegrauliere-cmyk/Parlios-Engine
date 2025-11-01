# Architecture (v4)

Flux principal :
1) **Clarifier** → pose 1–3 questions si flou.
2) **Briefing** → structure la demande (Brief JSON).
3) **RAG (Hybrid)** → TF‑IDF + BM25, citations obligatoires, rerank optionnel.
4) **Producer** → réponse alignée au **profil dynamique**.
5) **Verifier** → cohérence + règles du Brief.
6) **Meta‑Reflect** → score structure/concision/citations et notes.
