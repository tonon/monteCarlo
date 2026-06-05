PYTHON = .venv/bin/python3
PIP = .venv/bin/pip

.PHONY: help install sample run dash clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Ambiente pronto. Edite o .env se quiser usar Trello."

sample:
	mkdir -p data
	$(PYTHON) generate_sample_data.py

run:
	$(PYTHON) main.py

dash:
	$(PYTHON) -m streamlit run app.py

clean:
	rm -rf .venv
	rm -f kanban_local.db
	find . -type d -name "__pycache__" -exec rm -rf {} +