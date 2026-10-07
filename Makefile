.PHONY: clean clean-all codex


clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	
clean-all:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .venv/
	rm -rf .codex
	rm -rf node_modules/

codex:
	npm install @openai/codex --save-dev
	rm package.json package-lock.json
	npx codex