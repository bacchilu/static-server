.PHONY: clean clean-all codex run build update

STORAGE ?= FS
UPLOAD_DIRECTORY ?= /tmp/static-server-uploads


clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	
clean-all:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .venv/
	rm -rf .codex
	rm -rf node_modules/

run:
	STORAGE="$(STORAGE)" UPLOAD_DIRECTORY="$(UPLOAD_DIRECTORY)" .venv/bin/fastapi dev src/main.py

build:
	python3 -m venv .venv
	.venv/bin/python -m pip install -r requirements-lock.txt

update:
	python3 -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt
	.venv/bin/python -m pip freeze > requirements-lock.txt

codex:
	npm install @openai/codex --save-dev
	rm package.json package-lock.json
	npx codex
