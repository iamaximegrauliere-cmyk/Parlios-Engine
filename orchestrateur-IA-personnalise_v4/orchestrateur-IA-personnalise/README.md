# orchestrateur-IA-personnalise

Orchestrateur **multi-agents** ultra-personnalisé (profil dynamique + RAG + citations) basé sur ta méthode.

## 🚀 Démarrage rapide
```bash
# 1) (Optionnel) créer un venv
python -m venv .venv && source .venv/bin/activate

# 2) Installer les dépendances
pip install -r requirements.txt

# 3) Lancer l'API (FastAPI + Uvicorn)
uvicorn src.app.main:app --reload --port 8080

# 4) Construire l'index RAG (si tu as des docs)
python scripts/build_index.py --input ./data/docs --index ./data/index.pkl
```

## 📦 Structure
```
src/
  app/           # FastAPI endpoints
  orchestrator/  # Cerveau : planification, brief, routing
  agents/        # Agents spécialisés (briefing, recherche, production, vérif)
  rag/           # Ingestion/index/retrieval + citations
  memory/        # Profil utilisateur dynamique + mémoire courte/longue
  schemas/       # Pydantic models (Brief, Profil, etc.)
configs/         # YAML (persona, thinking framework, config serveur)
prompts/         # Prompts système/refus (se basent sur les YAML)
data/            # examples.jsonl, docs, index
scripts/         # scripts utilitaires (build index, eval)
tests/           # tests unitaires (base)
docs/            # notes d’archi, diagrammes
```

## 🔧 Endpoints clés
- `POST /ask` → prend `question` (+ option profil) et orchestre agents → **réponse avec citations**.
- `POST /brief` → transforme une demande floue en **Brief JSON** (actionnable).
- `POST /run` → exécute un **Brief** existant (pipeline agents).
- `POST /verify` → vérifie une réponse par rapport au **Brief**.
- `POST /profile/event` → ingère un signal faible (ajuste le profil).

## 🧠 Personnalisation
- Modifie `configs/persona.yaml` et `configs/thinking_framework.yaml`.
- Ajoute 20–50 paires dans `data/examples.jsonl` (style & réflexes).
- Place tes docs dans `data/docs/` puis construis l’index (`scripts/build_index.py`).

## ✅ Citations obligatoires
Le module RAG attache systématiquement `source` (fichier + page/section) aux extraits utilisés.
L’orchestrateur **refuse** d’émettre des affirmations factuelles non sourcées (ou marque `[à valider]`).

## 🧪 Évaluation
Utilise `scripts/evaluate.py` (exactitude@k, hallucinations, utilité, latence p95).


---
## ✅ 100% GitHub Ready

- Repo auto‑suffisant (pas d'appels externes obligatoires).
- Agents **Clarifier** et **Meta‑Reflect** inclus et activés.
- Script `scripts/generate_dashboard.py` pour produire `docs/dashboard.md`.
- Dossier `prompts/gold/` pour centraliser tes prompts exemplaires.
- Dossier `ventures/ventures.json` pour cartographier tes idées/projets.

### (Optionnel) GitHub Actions
Crée `.github/workflows/ci.yml` pour:
- lancer tests,
- générer le dashboard,
- publier les artefacts.


### Construire l'index RAG (TF-IDF local, léger)
```bash
python scripts/build_index.py --input ./data/docs --index ./data/index.pkl
```


## v4 — Nouveautés
- **RAG Hybride (TF‑IDF + BM25)** avec *rerank* optionnel.
- **Splitters** hiérarchiques (`src/rag/splitters.py`).
- **Évaluation rapide** (`eval/run_eval.py` + `eval/dataset.jsonl`) → `docs/eval_report.json`.
- **Docker multi‑stage** + **CI** avec cache pip et **smoke eval**.
- **Docs** : `docs/architecture.md`, `docs/operational-playbook.md`.
