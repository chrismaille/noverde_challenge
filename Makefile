pre_install:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	npm i -g serverless

install:
	poetry install

test:
	poetry run pytest

ci:
	poetry run pytest --cov=NoverdeChallenge  --black --mypy --pydocstyle --pycodestyle