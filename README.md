# Parlios-Engine

Orchestrateur IA **GitHub-native** : clarifie → planifie → valide → mémorise.

**Endpoints**: `/health`, `/ready`, `/run` (POST).

## Lancer local
```bash
make dev && make run
# http://localhost:8080/health
```

## Lancer en Docker
```bash
docker build -t parlios-engine .
docker run -p 8080:8080 parlios-engine
```

## Parler au cerveau depuis GitHub (ChatOps)
- **Append** : `/append prompts/briefs.md <BASE64>` → crée une PR d’ajout de contenu.
- **Delete** : `/delete prompts/old.md` → PR de suppression.
- **Trigger** : `/trigger daily-digest` → crée `.trigger/ua_core_dispatch/daily-digest_<ts>.txt`.

> **Note** : les workflows référencent uniquement **les secrets de ta GitHub App**. Aucun secret n8n n’est requis.

## Mémoire
Les sessions sont versionnées dans `.ua/memory/`.
Des snapshots/heartbeats peuvent être activés via workflows inclus (hardening).

## Tests
```bash
pytest -q
```
