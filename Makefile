.DEFAULT_GOAL := help

venv:
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv venv --python 3.12


.PHONY: install
install: venv ## Install all dependencies (in the virtual environment) defined in requirements.txt
	@uv pip install --upgrade pip
	@uv pip install -r requirements.txt


.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort


.PHONY: test
test: ## Run all notebooks in a test
	#export PYTHONWARNINGS="default"
	@uv pip install pytest
	@uv run pytest src/tests

.PHONY: cradle
cradle: install ## Run the cradle app
	./.venv/bin/python -m script

#./.venv/bin/python -m script