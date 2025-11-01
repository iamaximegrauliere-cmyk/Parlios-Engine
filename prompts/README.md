# Parlios Engine

[![CI](https://github.com/iamaximegrauliere-cmyk/Parlios-Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/iamaximegrauliere-cmyk/Parlios-Engine/actions/workflows/ci.yml)

API FastAPI pour orchestrer les agents Parlios (health/ready/run).

## Quickstart (Windows)

```powershell
# À la racine du repo
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install "uvicorn[standard]" fastapi pydantic requests pytest

$env:PYTHONPATH = (Get-Location).Path
python -m uvicorn engine.api.main:app --host 127.0.0.1 --port 8080
