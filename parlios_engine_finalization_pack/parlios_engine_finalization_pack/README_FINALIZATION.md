# Parlios Engine – Finalization Pack

## Contenu
- `engine/agents/` — stubs d'agents (clarify, planner, research, writer, validator)
- `app/security.py` — vérification Bearer optionnelle via `PARLIOS_API_KEY`
- `patches/ORCHESTRATOR_INTEGRATION_GUIDE.md` — guide pour brancher les agents dans votre orchestrateur
- `tests/test_flow.py` — test d'intégration minimal
- `.github/workflows/ci.yml` — CI simple pour pytest

## Étapes
1. **Copier** ce pack à la racine du repo (les chemins sont relatifs).
2. **Brancher** les imports et le pipeline comme indiqué dans `patches/ORCHESTRATOR_INTEGRATION_GUIDE.md`.
3. **(Optionnel)** Sécuriser `/run` avec `PARLIOS_API_KEY` et ajouter `Depends(require_api_key)`.
4. **Pousser une branche** et ouvrir une PR — la CI doit passer.
5. **Tester** via cURL ou le client Python.

## Test rapide (cURL)
Voir `docs/curl_cheatsheet.md` du Ops Kit.