.PHONY: setup test run-api run-dashboard docker-up docker-down clean

# Variables
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

setup:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest --cov=src --cov=api tests/

run-api:
	$(PYTHON) -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

run-dashboard:
	$(PYTHON) -m streamlit run dashboard/app.py

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
