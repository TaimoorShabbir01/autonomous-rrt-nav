.PHONY: venv run

venv:
	python -m venv .venv && . .venv/bin/activate || .\.venv\Scripts\activate && pip install -U pip && pip install -r requirements.txt

run:
	python src/main.py
