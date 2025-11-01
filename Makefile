.PHONY: venv install run run_secure test smoke clean

VENV=.venv
PY=$(VENV)/Scripts/python.exe
PIP=$(VENV)/Scripts/pip.exe

venv:
	py -3.11 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install "uvicorn[standard]" fastapi pydantic requests pytest

run:
	set PYTHONPATH=. && $(PY) -m uvicorn engine.api.main:app --host 127.0.0.1 --port 8080

run_secure:
	set PARLIOS_API_KEY=secret && set PYTHONPATH=. && $(PY) -m uvicorn engine.api.main:app --host 127.0.0.1 --port 8080

test:
	$(PY) -m pytest -q

smoke:
	powershell -ExecutionPolicy Bypass -File scripts/smoke.ps1

clean:
	@if exist .ua rmdir /s /q .ua
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist __pycache__ rmdir /s /q __pycache__
