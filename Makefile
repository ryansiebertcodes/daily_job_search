.PHONY: run install freeze clean

include .env
export

run:
	python3 src/fetch_resumes.py

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
