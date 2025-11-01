# Playbook Opérationnel

## Index RAG
```bash
python scripts/build_index.py --input ./data/docs --index ./data/index.pkl
```

## Lancer l'API
```bash
uvicorn src.app.main:app --reload --port 8080
```

## Évaluation rapide (local)
```bash
python eval/run_eval.py  # écrit docs/eval_report.json
```

## Docker
```bash
docker compose up --build
```

## CI (GitHub Actions)
- Lint + Tests
- Build index
- Génération dashboard (artifact)
