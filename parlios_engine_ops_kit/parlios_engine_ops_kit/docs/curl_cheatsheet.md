# Parlios Engine – cURL Cheat Sheet

> Remplacez `http://localhost:8080` par l'URL de votre déploiement.

## Health
```bash
curl -s http://localhost:8080/health | jq .
```

## Ready
```bash
curl -s http://localhost:8080/ready | jq .
```

## Run (requête simple)
```bash
curl -s -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Rédige un plan d'article sur l'orchestration IA.",
    "prefs": {"tone":"pro","length":"short","format":"markdown"},
    "session_id": "demo-001"
  }' | jq .
```

## Run (avec clé API)
```bash
curl -s -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PARLIOS_API_KEY" \
  -d '{
    "query": "Synthétise les points clés de la dernière session.",
    "prefs": {"tone":"neutral","length":"medium"},
    "session_id": "demo-002"
  }' | jq .
```