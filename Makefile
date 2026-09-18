.PHONY: install run lint format typecheck check clean

install: ## Install dependencies
	uv sync

run: ## Build chart and open in browser
	uv run python -m chart_builder

lint: ## Run ruff linter
	uv run ruff check src/

format: ## Run ruff formatter
	uv run ruff format src/

typecheck: ## Run mypy type checker
	uv run mypy src/

check: lint typecheck ## Run all checks (lint + typecheck)

clean: ## Remove generated artifacts
	rm -rf .venv/ dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
