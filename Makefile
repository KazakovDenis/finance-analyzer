fmt:
	poetry run ruff format

lint:
	poetry run ruff check
	poetry run mypy src/
