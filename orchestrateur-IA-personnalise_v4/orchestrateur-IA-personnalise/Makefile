.PHONY: setup run index test lint dashboard docker
setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run:
	uvicorn src.app.main:app --reload --port 8080

index:
	python scripts/build_index.py --input ./data/docs --index ./data/index.pkl

test:
	pytest -q

lint:
	ruff check . || true

dashboard:
	python scripts/generate_dashboard.py

docker:
	docker compose up --build
