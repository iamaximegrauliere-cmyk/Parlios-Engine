# Parlios Engine – cURL Cheat Sheet

> Remplacez `http://localhost:8080` par l'URL de votre déploiement.

## Health
```bash
curl -s http://localhost:8080/health | jq .
