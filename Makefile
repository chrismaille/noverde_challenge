pre_install:
	pip install -U --user poetry
	touch requirements.txt

install:
	python -m poetry install
	npm install

test:
	poetry run pytest

ci:
	python -m poetry run pytest --cov=noverde_challenge --black --mypy --pydocstyle --pycodestyle --ignore=node_modules