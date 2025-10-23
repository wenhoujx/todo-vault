# Variables
PYTHON = uv run
CDK = $(PYTHON) cdk
FRONTEND_DIR = frontend
BACKEND_DIR = server

# Default target
all: help

## ---------- ENV ----------
venv:
	uv venv --python 3.12
	uv sync

clean:
	rm -rf .venv .pytest_cache __pycache__ cdk.out

## ---------- BACKEND (CDK) ----------
deploy:
	$(CDK) deploy

synth:
	$(CDK) synth

destroy:
	$(CDK) destroy --force

diff:
	$(CDK) diff

## ---------- FRONTEND ----------
build-fe:
	npm run build

install-fe:
	npm install

dev-fe:
	npm run dev

## ---------- PYTHON ----------
lint:
	$(PYTHON) ruff check .

format:
	$(PYTHON) ruff format .

test:
	$(PYTHON) pytest -q

## ---------- UTIL ----------
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
