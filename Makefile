.PHONY: dev run test build fmt
dev:
	python -m pip install -U pip wheel
	pip install -r requirements.txt

run:
	uvicorn engine.api.main:app --host 0.0.0.0 --port 8080

test:
	pytest -q

build:
	docker build -t parlios-engine:latest .

fmt:
	ruff check --fix .
