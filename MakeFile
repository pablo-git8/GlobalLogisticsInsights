.PHONY: all install venv format lint security run-scripts clean streamlit

VENV := venv

SCRIPTS_DIR := scripts

install: 
	@echo "Installing requirements..."
		python3.10 -m venv $(VENV) && \
		source venv/bin/activate && \
		pip install -r requirements.txt


format:
	@echo "Running Python scripts..."
	@for script in $(wildcard $(SCRIPTS_DIR)/*.py); do \
		echo "Executing $$script"; \
		black $$script; \
	done

lint:
	@echo "Running Python scripts..."
	@for script in $(wildcard $(SCRIPTS_DIR)/*.py); do \
		echo "Executing $$script"; \
		flake8 $$script --count --select=E9,F63,F7,F82 --show-source --statistics; \
		flake8 $$script --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics; \
	done

security:
	@echo "Running Python scripts..."
	@for script in $(wildcard $(SCRIPTS_DIR)/*.py); do \
		echo "Executing $$script"; \
		bandit -r $$script --tests B101; \
	done

run-scripts:
	@echo "Running Python scripts..."
	@for script in $(wildcard $(SCRIPTS_DIR)/*.py); do \
		echo "Executing $$script"; \
		python $$script; \
	done

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

streamlit: 
	python -m streamlit run news_app/app.py

all: install format lint security run-scripts clean streamlit
