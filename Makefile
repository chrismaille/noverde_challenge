pre_install:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	sudo npm i -g serverless

install:
	poetry install
	npm install

test:
	poetry run pytest

ci:
	poetry run pytest --cov=noverde_challenge --black --mypy --pydocstyle --pycodestyle --ignore=node_modules
