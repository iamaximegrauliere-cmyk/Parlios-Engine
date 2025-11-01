# Parlios Engine – Ops Guide

## 1) Déploiement rapide
- Local: `make dev && make run` → endpoints `/health`, `/ready`, `/run`
- Docker: `docker build -t parlios-engine . && docker run -p 8080:8080 parlios-engine`

## 2) Sécurité API (recommandé)
- Activer une vérification d'en-tête `Authorization: Bearer <token>` côté FastAPI (dépendance) et variable d'env `PARLIOS_API_KEY`.
- Limiter `POST /run` aux requêtes authentifiées.

## 3) ChatOps (GitHub-native)
- Placez les workflows dans `.github/workflows/`.
- Commandes dans des commentaires d'issue/PR:
  - `/append <path> <BASE64>` → crée une PR d'ajout de contenu.
  - `/delete <path>` → PR de suppression du fichier.
  - `/trigger <name>` → crée `.trigger/ua_core_dispatch/<name>_<ts>.txt` et pousse une branche dédiée.

## 4) Clients
- Python: `parlios_client.py`
- cURL: voir `curl_cheatsheet.md`

## 5) Bonnes pratiques
- Versionner les sessions dans `.ua/memory/` (déjà géré par l'engine).
- Ajouter des agents effecteurs: Recherche, Rédaction, Code. Brancher dans `_execute` via un plan exécutable.
- Ajouter des golden tests dans `prompts/`.